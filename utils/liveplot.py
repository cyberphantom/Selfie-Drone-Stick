#!/usr/bin/env python
import matplotlib
matplotlib.use
import matplotlib.pyplot as plt
import gym
import rospkg
rewards_key = 'episode_rewards'

class LivePlot(object):
    def __init__(self, outdir, data_key=rewards_key, line_color='blue'):
        """
        Liveplot renders a graph of either episode_rewards or episode_lengths
        Args:
            outdir (outdir): Monitor output file location used to populate the graph
            data_key (Optional[str]): The key in the json to graph (episode_rewards or episode_lengths).
            line_color (Optional[dict]): Color of the plot.
        """
        self.outdir = outdir
        self.data_key = data_key
        self.line_color = line_color

        #styling options
        matplotlib.rcParams['toolbar'] = 'None'
        plt.style.use('ggplot')
        plt.xlabel("Episodes")
        plt.ylabel(data_key)
        fig = plt.gcf().canvas.set_window_title('simulation_graph')

    def plot(self, env):
        if self.data_key is rewards_key:
            data = gym.wrappers.Monitor.get_episode_rewards(env)
        else:
            data = gym.wrappers.Monitor.get_episode_lengths(env)

        plt.plot(data, color=self.line_color)

        # pause so matplotlib will display
        # may want to figure out matplotlib animation or use a different library in the future
plt.pause(0.000001)




if __name__ == '__main__':
    print matplotlib.__version__
    rospack = rospkg.RosPack()
    pkg_path = rospack.get_path('reinforced_selfiestickdrone')
    outdir = pkg_path + '/droneQlearning_trainingLogs'
    # outdir = '/home/saif/catkin_ws/src/reinforced_selfiestickdrone/training_results/new/'
    plotter = LivePlot(outdir)

