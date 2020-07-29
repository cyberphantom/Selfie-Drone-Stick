#!/usr/bin/env python

__Author__ = "Saif Alalbachi"

# ROS import
import future
import rospy
import rospkg
from geometry_msgs.msg import Twist, Vector3Stamped, Pose, PoseWithCovarianceStamped
from sensor_msgs.msg import Imu
#from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Empty
# Required Libraries
import time, csv
import math
import random
import numpy as np
import cPickle as pickle
from collections import deque # Ordered collection with ends
import gym
import pandas
from gym import wrappers
import tensorflow as tf
from lib.exp_replay import Memory
from lib.get_next_obs import nextObs
from lib.architecture import grade_dec_drone_net

# Reinforcement Learning Algs.

def discount_and_normalize_rewards(ep_re, gamma = 0.99):
    dis_re = np.zeros_like(ep_re)
    cumulative = 0.0
    for i in reversed(xrange(len(ep_re))):
        cumulative = cumulative * gamma + ep_re[i]
        dis_re[i] = cumulative

    mean = np.mean(dis_re)
    std = np.std(dis_re)
    dis_re = (dis_re - mean) / (std)

    return dis_re

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))  # sigmoid "squashing" function to interval [0,1]

def softmax(x):
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  return probs

def stack_ob(stacked_obs, bined_ob, is_new_episode):
    # Preprocess frame
    bOB = bined_ob

    if is_new_episode:
        # Clear our stacked_frames
        stacked_obs = deque([np.zeros((1, 4), dtype=np.int) for _ in range(Stack_Size)], maxlen=4)
        # Because we're in a new episode, copy the same frame 4x
        stacked_obs.append(bOB)
        stacked_obs.append(bOB)
        stacked_obs.append(bOB)
        stacked_obs.append(bOB)

        # Stack the frames
        stacked_state = np.stack(stacked_obs, axis=1)

    else:
        # Append frame to deque, automatically removes the oldest frame
        stacked_obs.append(bOB)

        # Build the stacked state (first dimension specifies different frames)
        #print(stacked_obs)
        stacked_state = np.stack(stacked_obs, axis=1)
        #print(stacked_state)
    return stacked_state, stacked_obs


def make_batch(stacked_ob):
    # Initialize lists: states, actions, rewards_of_episode, rewards_of_batch, discounted_rewards
    stacked_states, actions, rewards_of_episode, rewards_of_batch, discounted_rewards = [], [], [], [], []

    # Reward of batch is also a trick to keep track of how many timestep we made.
    # We use to to verify at the end of each episode if > batch_size or not.

    # Keep track of how many episodes in our batch (useful when we'll need to calculate the average reward per episode)
    episode_num = 1

    bined_observation = []
    while len(bined_observation) == 0:
        bined_observation = env.reset()
        start_time = time.time()
    stacked_state, stacked_ob = stack_ob(stacked_ob, bined_observation, True)
    #print("current obs: ", bined_observation)

    while True:
        # Run State Through Policy & Calculate Action
        action_probability_distribution = sess.run(gddNet.action_distribution,
                                                   feed_dict={gddNet.inputs_: stacked_state.reshape(1, 1, 4, 4)})

        # REMEMBER THAT WE ARE IN A STOCHASTIC POLICY SO WE DON'T ALWAYS TAKE THE ACTION WITH THE HIGHEST PROBABILITY
        # (For instance if the action with the best probability for state S is a1 with 70% chances, there is
        # 30% chance that we take action a2)
        # print(action_probability_distribution.shape[3])
        # print(action_probability_distribution[0][0][1])
        # for _ in range(action_probability_distribution.shape[1]):
        #     print("ss")

        #print(action_probability_distribution.shape[1])
        #print(action_probability_distribution)
        action = 16  # select action w.r.t the actions prob

        # Perform action
        bined_observation, reward, done, info = env.step(action)
        action = possible_actions[action]

        # Store results
        stacked_states.append(stacked_state)
        actions.append(action)
        rewards_of_episode.append(reward)

        #print("rewards_of_episode", rewards_of_episode, type(reward))
        if done:
            #next_ob = np.squeeze(np.zeros((1, 4), dtype=np.int)).tolist()
            next_ob = np.squeeze([2, 3, 3, 3]).tolist()
            # print(stacked_ob)
            # print(next_ob)
            next_stacked_state, stacked_ob = stack_ob(stacked_ob, next_ob, False)

            # Append the reward_of_episode to rewards_of_batch
            rewards_of_batch.append(rewards_of_episode)
            #print("rewards_of_batch", rewards_of_batch)
            # Calculate gamma Gt
            discounted_rewards.append(discount_and_normalize_rewards(rewards_of_episode))

            # If the number of rewards_of_batch > batch_size stop the minibatch creation
            # (Because we have sufficient number of episode mb)
            # Remember that we put this condition here, because we want entire episode (Monte Carlo)
            # so we can't check that condition for each step but only if an episode is finished
            #print("step: ", len(np.concatenate(rewards_of_batch)))
            if len(np.concatenate(rewards_of_batch)) > batch_size:
                break

            # Reset the transition stores
            rewards_of_episode = []

            # Add episode
            episode_num += 1

            #state, stacked_ob = stack_ob(stacked_ob, bined_observation, True)
            bined_observation_reset = env.reset()

            if len(bined_observation_reset) != 0:
                bined_observation = bined_observation_reset

            if len(bined_observation) == 0:
                #bined_observation = np.squeeze(np.zeros((1, 4), dtype=np.int)).tolist()
                bined_observation = np.squeeze([2, 3, 3, 3]).tolist()
            stacked_state, stacked_ob = stack_ob(stacked_ob, bined_observation, True)

        else:
            # If not done, the next_state become the current state
            #next_ob = bined_observation
            next_ob = nextObs()
            # first check if next = 0 then check if current  = 0 then put 0
            if len(bined_observation) == 0 and len(next_ob) ==0:
                #next_ob = np.squeeze(np.zeros((1, 4), dtype=np.int)).tolist()
                next_ob = np.squeeze([2, 3, 3, 3]).tolist()

            elif len(next_ob) == 0 and len(bined_observation) != 0:
                next_ob = bined_observation

            #print("next_observation", next_ob, bined_observation)
            next_stacked_state, stacked_ob = stack_ob(stacked_ob, next_ob, False)
            stacked_state = next_stacked_state

        #print("episode: ", episode_num)
        #print("discounted_rewards: ", discounted_rewards, "len: ", len(discounted_rewards))

    return np.stack(np.array(stacked_states)), np.stack(np.array(actions)), np.concatenate(rewards_of_batch), np.concatenate(
        discounted_rewards), episode_num

if __name__ == '__main__':

    # Node Initialization
    rospy.init_node('Selfie-Drone-Stick')

    # Create the Environmet (with the same name as in mydrone_end)
    env = gym.make('reinforcedDrone-v0')
    rospy.loginfo("Gym Environment Initialized")

    # Set the logging system
    rospack = rospkg.RosPack()
    pkg_path = rospack.get_path('Selfie-Drone-Stick')
    outdir = pkg_path + '/gdTrainingLog/'

    #bridge = CvBridge()

    # Load training parameters from the yaml file
    Alpha = rospy.get_param("/alpha")
    Gamma = rospy.get_param("/gamma")
    Learning_Rate = rospy.get_param("/learning_rate")
    Decay_Rate = rospy.get_param("/decay_rate")
    batch_size = rospy.get_param("/batch_size")
    Nsteps = rospy.get_param("/stepsTH")
    memory_size = rospy.get_param("/memory_size")

    ### ENVIRONMENT HYPERPARAMETERS
    resume = rospy.get_param("/resume")  # Resume from previous checkpoint
    Stack_Size = rospy.get_param("/stack_size")  # Defines how many frames are stacked together
    action_size = env.action_space.n  # 55 possible actions
    possible_actions = np.identity(action_size, dtype=int).tolist()

    ## TRAINING HYPERPARAMETERS
    #state_size = 1 * 4 * int(Stack_Size)  # Input Obs Dim
    stacked_state_size = [1, 4, int(Stack_Size)]  # Input Obs Dim

    # Check init state binned values
    #stacked_ob = deque([np.zeros((1, 4), dtype=np.int) for _ in range(Stack_Size + 1)], maxlen=4)
    stacked_ob = deque([[2, 3, 3, 3] for _ in range(Stack_Size + 1)], maxlen=4)

    # Reset the graph
    tf.reset_default_graph()

    # Instantiate the Network
    gddNet = grade_dec_drone_net(stacked_state_size, action_size, Learning_Rate)

    # Initialize Session
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    ### MODIFY THIS TO FALSE IF YOU JUST WANT TO SEE THE TRAINED AGENT
    training = True

    # Setup TensorBoard Writer
    #writer = tf.summary.FileWriter("./tensorboard/pg/test2")
    writer = tf.summary.FileWriter(outdir + "tensorboard/")

    ## Losses
    tf.summary.scalar("Loss", gddNet.loss)

    ## Reward mean
    tf.summary.scalar("Reward_mean", gddNet.mean_reward_)

    write_op = tf.summary.merge_all()

    # Keep track of all rewards total for each batch
    allRewards = []
    total_rewards = 0
    maximumRewardRecorded = 0
    mean_reward_total = []
    epoch = 1
    average_reward = []

    # Saver
    saver = tf.train.Saver()
    data_file = []
    data_file.append(["Epoch", "Number of training episodes", "Total reward", "Mean Reward of that batch",
                      "Average Reward of all training", "Max reward for a batch so far", "Loss"])
    if training:

        if resume:
            # Load the model
            saver.restore(sess, outdir + "models/gdDrone.ckpt")

        while True:

            # Gather training data
            stacked_states_mb, actions_mb, rewards_of_batch, discounted_rewards_mb, nb_episodes_mb = make_batch(stacked_ob)
            ### These part is used for analytics
            # Calculate the total reward ot the batch
            total_reward_of_that_batch = np.sum(rewards_of_batch)
            allRewards.append(total_reward_of_that_batch)

            # Calculate the mean reward of the batch
            # Total rewards of batch / nb episodes in that batch
            mean_reward_of_that_batch = np.divide(total_reward_of_that_batch, nb_episodes_mb)
            mean_reward_total.append(mean_reward_of_that_batch)

            # Calculate the average reward of all training
            # mean_reward_of_that_batch / epoch
            average_reward_of_all_training = np.divide(np.sum(mean_reward_total), epoch)

            # Calculate maximum reward recorded
            maximumRewardRecorded = np.amax(allRewards)

            print("==========================================")
            print("Epoch: ", epoch)
            print("-----------")
            print("Number of training episodes: {}".format(nb_episodes_mb))
            print("Total reward: {}".format(total_reward_of_that_batch, nb_episodes_mb))
            print("Mean Reward of that batch {}".format(mean_reward_of_that_batch))
            print("Average Reward of all training: {}".format(average_reward_of_all_training))
            print("Max reward for a batch so far: {}".format(maximumRewardRecorded))
            loss_, _ = sess.run([gddNet.loss, gddNet.train_opt],
                                feed_dict={gddNet.inputs_: stacked_states_mb.reshape((len(stacked_states_mb), 1, 4, 4)),
                                           gddNet.actions: actions_mb,
                                           gddNet.discounted_episode_rewards_: discounted_rewards_mb
                                           })

            print("Training Loss: {}".format(loss_))
            data_file.append([epoch, nb_episodes_mb, total_reward_of_that_batch, mean_reward_of_that_batch,
                              average_reward_of_all_training, maximumRewardRecorded, loss_])

            with open(outdir + 'log.csv', 'w') as fout:
                csvwriter = csv.writer(fout)
                csvwriter.writerows(data_file)
            fout.close()

            # Write TF Summaries
            summary = sess.run(write_op, feed_dict={gddNet.inputs_: stacked_states_mb.reshape((len(stacked_states_mb), 1, 4, 4)),
                                                    gddNet.actions: actions_mb,
                                                    gddNet.discounted_episode_rewards_: discounted_rewards_mb,
                                                    gddNet.mean_reward_: mean_reward_of_that_batch})

            # summary = sess.run(write_op, feed_dict={x: s_.reshape(len(s_),84,84,1), y:a_, d_r: d_r_, r: r_, n: n_})
            writer.add_summary(summary, epoch)
            writer.flush()


            # Save Model
            if epoch % 10 == 0:
                #str(epoch)
                saver.save(sess, outdir + "models/gdDrone" + str(epoch) +".ckpt")
                print("Model saved")
            epoch += 1