#!/usr/bin/env python

__Author__ = "Saif Alalbachi"

# ROS import
import rospy
import rospkg
from geometry_msgs.msg import Twist, Vector3Stamped, Pose, PoseWithCovarianceStamped
from sensor_msgs.msg import Imu
#from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Empty
# Required Libraries
import time, csv
import random
import numpy as np
import skimage
from collections import deque # Ordered collection with ends
from gym import wrappers
import tensorflow as tf
from lib.exp_replay import Memory
from lib.get_next_obs import nextObs
from lib.sdsnet import DDDQNNet
from lib.memory import SumTree, Memory
import env_sds
from ast import literal_eval

import warnings
import gym

warnings.filterwarnings('ignore')


def stack_ob(bined_ob, obs= None):
    # Preprocess frame
    bOB = bined_ob

    if obs is None:
        # Clear our stacked_frames

        obs = deque([bOB for _ in range(stack_size)], maxlen=4)

        # Stack the frames
        stacked_state = np.stack(obs, axis=1)

    else:
        # Append frame to deque, automatically removes the oldest frame
        obs.append(bOB)

        # Build the stacked state (first dimension specifies different frames)
        stacked_state = np.stack(obs, axis=1)

    stacked_s = np.expand_dims(stacked_state, 0)
    return stacked_s, obs


def predict_action(sess, explore_start, explore_stop, decay_rate, decay_step, s_state):
    ## EPSILON GREEDY STRATEGY
    # Choose action a from state s using epsilon greedy.
    ## First we randomize a number
    exp_exp_tradeoff = np.random.rand()

    # Here we'll use an improved version of our epsilon greedy strategy used in Q-learning notebook
    explore_probability = explore_stop + (explore_start - explore_stop) * np.exp(-decay_rate * decay_step)

    if (explore_probability > exp_exp_tradeoff):
        # Make a random action (exploration)
        action = random.choice(possible_actions)

    else:
        # Get action from Q-network (exploitation)
        # Estimate the Qs values state
        Qs = sess.run(DQNetwork.output, feed_dict={DQNetwork.inputs_: np.expand_dims(s_state, 0)})

        # Take the biggest Q value (= the best action)
        choice = np.argmax(Qs)
        action = possible_actions[int(choice)]

    return action, explore_probability


def make_batch():
    for i in range(4*batch_size):
        # If it's the first step
        # First we need a state
        state = env.reset()
        stacked_state, obs = stack_ob(state)
        step = 0

        while step <= nsteps:

            # Random action
            action = random.choice(possible_actions)
            act = possible_actions.index(action)

            # Get the rewards
            next_state, reward, done, drone_shot = env.step(act)
            if len(next_state) > 4:

                step += 1

                next_stacked_state, next_obs = stack_ob(next_state, obs)
                memory.store((stacked_state, action, reward, next_stacked_state, done))

                # If we're dead
                if done:
                    step = nsteps + 1

                else:
                    stacked_state = next_stacked_state
                    obs = next_obs
            else:
                step = nsteps + 1


# This function helps us to copy one set of variables to another
# In our case we use it when we want to copy the parameters of DQN to Target_network
# Thanks of the very good implementation of Arthur Juliani https://github.com/awjuliani
def update_target_graph():
    # Get the parameters of our DQNNetwork
    from_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, "DQNetwork")

    # Get the parameters of our Target_network
    to_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, "TargetNetwork")

    op_holder = []

    # Update our target_network parameters with DQNNetwork parameters
    for from_var, to_var in zip(from_vars, to_vars):
        op_holder.append(to_var.assign(from_var))
    return op_holder


def main():

    saver = tf.train.Saver()

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    if training:

        if not resume:
            make_batch()

        writer = tf.summary.FileWriter(outdir + "tensorboard/")

        ## Losses
        tf.summary.scalar("Loss", DQNetwork.loss)

        write_op = tf.summary.merge_all()
        epoch = 1
        loss = None
        sumsEpsR = []
        avgsEpsR = []
        total_rewards = 0
        average_reward = []
        maxRRec, avgR = None, None
        data_file = []
        if resume:
            # Load the model
            saver.restore(sess, outdir + "models/sds" + str(resume_ep) + ".ckpt")

        data_file.append(["Epoch", "Total reward", "Mean Reward of that batch", "Max reward for a batch so far",
                          "Loss", "Touch_down"])

        # Initialize the decay rate (that will use to reduce epsilon)
        decay_step = 0

        # Set tau = 0
        tau = 0

        # How many times we achieved the goal
        drone_shot = 0

        # Update the parameters of our TargetNetwork with DQN_weights
        update_target = update_target_graph()
        sess.run(update_target)

        for episode in range(total_episodes):

            step = 0
            # Initialize the rewards of the episode
            episode_rewards = []

            # Make a new episode and observe the first state
            state = env.reset()
            stacked_state, obs = stack_ob(state)

            while step <= nsteps:

                # Predict the action to take and take it
                action, explore_probability = predict_action(sess, explore_start, explore_stop, decay_rate, decay_step,
                                                             stacked_state)
                act = action.index(1)
                # Get the rewards
                next_state, reward, done, drone_shot = env.step(act)
                if len(next_state) > 4:

                    step += 1

                    # Increase the C step
                    tau += 1

                    # Increase decay_step
                    decay_step += 1

                    # print("reward", reward, "done", done, "state", next_state, "goal", drone_shot,
                    #       "action", act, "exp_prob", explore_probability)

                    next_stacked_state, next_obs = stack_ob(next_state, obs)
                    memory.store((stacked_state, action, reward, next_stacked_state, done))

                    # Add the reward to total reward
                    episode_rewards.append(reward)

                    # Get the total reward of the episode
                    total_reward = np.sum(episode_rewards)

                    # If the game is finished
                    if done:

                        sumsEpsR.append(total_reward)
                        avgsEpsR.append(total_reward / nsteps)

                        print('Episode: {}'.format(episode),
                              'Total reward: {}'.format(total_reward),
                              'Explore P: {:.4f}'.format(explore_probability),
                              'Target: {}'.format(next_state),
                              'step: {}'. format(step),
                              'Drone Shot: {}'.format(drone_shot))

                        step = nsteps + 1

                    else:
                        stacked_state = next_stacked_state
                        obs = next_obs
                else:
                    step = nsteps + 1


                ### LEARNING PART
                # Obtain random mini-batch from memory
                tree_idx, batch, ISWeights_mb = memory.sample(batch_size)
                stacked_states_mb = np.array([each[0][0] for each in batch], ndmin=3)
                actions_mb = np.array([each[0][1] for each in batch])
                rewards_mb = np.array([each[0][2] for each in batch])
                next_stacked_states_mb = np.array([each[0][3] for each in batch], ndmin=3)
                dones_mb = np.array([each[0][4] for each in batch])

                target_Qs_batch = []

                # Get Q values for next_state
                q_next_state = sess.run(DQNetwork.output, feed_dict={DQNetwork.inputs_: next_stacked_states_mb})

                # Calculate Qtarget for all actions that state
                q_target_next_state = sess.run(TargetNetwork.output, feed_dict={TargetNetwork.inputs_: next_stacked_states_mb})

                # Set Q_target = r if the episode ends at s+1, otherwise set Q_target = r + gamma*maxQ(s', a')
                for i in range(0, len(batch)):
                    terminal = dones_mb[i]

                    # We got a'
                    action = np.argmax(q_next_state[i])

                    # If we are in a terminal state, only equals reward
                    if terminal:
                        target_Qs_batch.append(rewards_mb[i])

                    else:
                        # Take the Qtarget for action a'
                        target = rewards_mb[i] + gamma * q_target_next_state[i][action]
                        target_Qs_batch.append(target)

                targets_mb = np.array([each for each in target_Qs_batch])

                _, loss, absolute_errors = sess.run([DQNetwork.optimizer, DQNetwork.loss, DQNetwork.absolute_errors],
                                    feed_dict={DQNetwork.inputs_: stacked_states_mb,
                                               DQNetwork.target_Q: targets_mb,
                                               DQNetwork.actions_: actions_mb,
                                               DQNetwork.ISWeights_: ISWeights_mb})

                # Update priority
                memory.batch_update(tree_idx, absolute_errors)

                # Write TF Summaries
                summary = sess.run(write_op, feed_dict={DQNetwork.inputs_: stacked_states_mb,
                                                   DQNetwork.target_Q: targets_mb,
                                                   DQNetwork.actions_: actions_mb,
                                              DQNetwork.ISWeights_: ISWeights_mb})

                writer.add_summary(summary, episode)
                writer.flush()

                if tau > max_tau:
                    # Update the parameters of our TargetNetwork with DQN_weights
                    update_target = update_target_graph()
                    sess.run(update_target)
                    tau = 0
                    print("Model updated")

            # Save model every 100 episodes
            if episode % 100 == 0 and episode > 0:
                save_path = saver.save(sess, outdir + "models/sds" + str(episode + resume_ep) + ".ckpt")
                maxRRec = np.amax(sumsEpsR)

                data_file.append([epoch, sumsEpsR[-1], avgsEpsR[-1], maxRRec, loss, drone_shot])

                with open(outdir + 'sdsLog.csv', 'w') as fout:
                    csvwriter = csv.writer(fout)
                    csvwriter.writerows(data_file)
                fout.close()

                epoch += 1

                print("Model Saved")

    else:

        # Load the model
        saver.restore(sess, outdir + "models/sds" + str(resume_ep) + ".ckpt")
        tre = 0

        for j in range(batch_size):

            tstp = 0
            tact = 0
            t_reward = []
            sumsR = []
            avgsR = []
            # Make a new episode and observe the first state
            tst = env.reset()
            tstkd_st, tobs = stack_ob(tst)
            g = False
            while tstp <= nsteps:


                if tre >= 2:
                    tact = 0
                    g = True

                if not g:

                    # Take the biggest Q value (= the best action)
                    tQs = sess.run(DQNetwork.output, feed_dict={DQNetwork.inputs_: np.expand_dims(tstkd_st, 0)})
                    # Take the biggest Q value (= the best action)
                    tchc = np.argmax(tQs)
                    taction = possible_actions[int(tchc)]

                    tact = taction.index(1)


                # Get the rewards
                tnxt_st, tre, tdon, tstp_c_gl = env.step(tact)

                if len(tnxt_st) > 2:
                    tstp += 1


                    tnxt_stkd_st, tnxt_tobs = stack_ob(tnxt_st, tobs)
                    t_reward.append(tre)

                    # print("reward", tre, "done", tdon, "state", tnxt_st, "goal", tstp_c_gl, "action", tact)




                    if tdon:

                        # sumsR.append(t_reward)
                        # avgsR.append(t_reward / nsteps)

                        print('Episode: {}'.format(j),
                              'Target: {}'.format(tnxt_st),
                              'step: {}'.format(tstp),
                              'Drone Shot: {}'.format(tstp_c_gl))

                        tstp = nsteps + 1

                    else:
                        print("reward= ", tre)
                        print("Target= ", tnxt_st)
                        tobs = tnxt_tobs

                else:
                    tstp = nsteps + 1

            print("Score: ", np.sum(t_reward))


if __name__ == '__main__':

    ### ROS HYPERPARAMETERS
    # Node Initialization
    rospy.init_node('Selfie-Drone-Stick')


    ### ENVIRONMENT HYPERPARAMETERS
    # Create the Environmet
    env = gym.make('sds-v0')
    #env.seed(1)  # reproducible
    env = env.unwrapped  # removes all the wrappers, enter the behind the scene dynamics
    rospy.loginfo("Gym Environment Initialized")


    ### TRAINING HYPERPARAMETERS
    # Load training parameters from the yaml file
    training = rospy.get_param("/training")  # Training or testing
    resume = rospy.get_param("/resume")  # Resume from previous checkpoint
    resume_ep = rospy.get_param("/resume_ep")
    OUTPUT_GRAPH = rospy.get_param("/output_graph")

    gamma = rospy.get_param("/gamma")
    explore_start = rospy.get_param("/explore_start")
    explore_stop = rospy.get_param("/explore_stop")
    decay_rate = rospy.get_param("/d_rate")
    learning_rate = rospy.get_param("/learning_rate")
    total_episodes = rospy.get_param("/episodesTH")
    batch_size = rospy.get_param("/batch_size")
    nsteps = rospy.get_param("/stepsTH")
    memory_size = rospy.get_param("/memory_size")
    max_tau = rospy.get_param("/tauTH")
    pretrain_length = batch_size

    stack_size = rospy.get_param("/stack_size")  # 4
    ob_size = rospy.get_param("/ob_size")  # 8
    stacked_state_size = [1, ob_size, stack_size] # Input Dim 1 * 8 * 4

    action_size = env.action_space.n  # 81 possible actions
    possible_actions = np.identity(action_size, dtype=int).tolist()


    # Reset the graph
    tf.reset_default_graph()

    # Instantiate the DQNetwork
    DQNetwork = DDDQNNet(action_size, learning_rate)

    # Instantiate the target network
    TargetNetwork = DDDQNNet(action_size, learning_rate, name="TargetNetwork")

    # Set the logging system
    rospack = rospkg.RosPack()
    pkg_path = rospack.get_path('Selfie-Drone-Stick')
    outdir = pkg_path + '/sds_norm/'

    # memory
    memory = Memory(memory_size)

    main()


