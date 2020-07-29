import tensorflow as tf

class DQNetwork:
    def __init__(self, action_size, learning_rate, name='DQNetwork'):
        self.state_size = [1, 4, 4]
        self.action_size = action_size
        self.learning_rate = float(learning_rate)

        with tf.variable_scope(name):
            # We create the placeholders
            # *state_size means that we take each elements of state_size in tuple hence is like if we wrote
            # [None, 84, 84, 4]
            self.inputs_ = tf.placeholder(tf.float32, [None, 1, 4, 4], name="inputs")
            self.actions_ = tf.placeholder(tf.float32, [None, action_size], name="actions_")

            # Remember that target_Q is the R(s,a) + ymax Qhat(s', a')
            self.target_Q = tf.placeholder(tf.float32, [None], name="target")


            self.flatten = tf.layers.flatten(self.inputs_)
            ## --> [1152]

            self.fc1 = tf.layers.dense(inputs=self.flatten,
                                      units=32,
                                      activation=tf.nn.elu,
                                      kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                      name="fc1")

            self.fc2 = tf.layers.dense(inputs=self.flatten,
                                      units=64,
                                      activation=tf.nn.elu,
                                      kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                      name="fc2")

            self.output = tf.layers.dense(inputs=self.fc2,
                                          kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                          units=action_size,
                                          activation=None)

            # Q is our predicted Q value.
            self.Q = tf.reduce_sum(tf.multiply(self.output, self.actions_), axis=1)

            # The loss is the difference between our predicted Q_values and the Q_target
            # Sum(Qtarget - Q)^2
            self.loss = tf.reduce_mean(tf.square(self.target_Q - self.Q))

            self.optimizer = tf.train.RMSPropOptimizer(self.learning_rate).minimize(self.loss)
