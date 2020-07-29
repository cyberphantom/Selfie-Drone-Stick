import tensorflow as tf

class grade_dec_drone_net:

    def __init__(self, state_size, action_size, learning_rate, name='dNet'):
        self.state_size = state_size
        self.action_size = int(action_size)
        self.learning_rate = float(learning_rate)

        with tf.variable_scope(name):

            with tf.name_scope("inputs"):
                self.inputs_ = tf.placeholder(tf.float32, [None, 1, 4, 4], name="inputs_")
                self.actions = tf.placeholder(tf.int32, [None, action_size], name="actions")
                self.discounted_episode_rewards_ = tf.placeholder(tf.float32, [None, ],
                                                                  name="discounted_episode_rewards_")
                # Add this placeholder for having this variable in tensorboard
                self.mean_reward_ = tf.placeholder(tf.float32, name="mean_reward")

            with tf.name_scope("flatten"):
                self.flatten = tf.layers.flatten(self.inputs_)


            with tf.name_scope("fc1"):
                self.fc1 = tf.layers.dense(inputs=self.flatten,
                                            units=32,
                                            activation = tf.nn.relu,
                                            kernel_initializer=tf.contrib.layers.xavier_initializer(), name="fc1")


            with tf.name_scope("logits"):
                self.logits = tf.layers.dense(inputs=self.fc1,
                                               units=self.action_size,
                                               activation=None)


            with tf.name_scope("softmax"):
                self.action_distribution = tf.nn.softmax(self.logits)

            # Not sure if I need to use V2, if we want to update labels, we should use tf.variables
            with tf.name_scope("loss"):
                self.neg_log_prob = tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.logits, labels=self.actions)
                self.loss = tf.reduce_mean(self.neg_log_prob * self.discounted_episode_rewards_)

            with tf.name_scope("train"):
                self.train_opt = tf.train.RMSPropOptimizer(self.learning_rate).minimize(self.loss)