import argparse
from ast import parse
import matplotlib.pyplot as plt



def default_argument_parser():
    """
    Create a parser.
    Returns:
        argparse.ArgumentParser:
    """
    parser = argparse.ArgumentParser(description="Squeezenet Plotting")
    parser.add_argument(
        "--nvidia-file",
        default="",
        metavar="FILE",
        help="path to nvidia log file",
    )
    parser.add_argument(
        "--dml-file",
        default="",
        help="path to dml log file",
    )

    parser.add_argument(
        "--plot-title",
        default="",
        help="title of plot"
    )

    parser.add_argument(
        "--plot-type",
        default="cost",
        help="the type of plot you want"
    )

    parser.add_argument(
        "--x-label",
        default="",
        help="label across x axis of graph"
    )

    parser.add_argument(
        "--y-label",
        default="",
        help="label across y axis of graph"
    )


    return parser

def parse_log_for_cumulative_cost(log_file, price):
    price_per_min = float(price / 43800)
    cost = []
    epochs = []
    epoch = 1
    cost_per_epoch = 0
    with open(log_file) as file:
        for line in file:
            if "took a total of" in line:
                epochs.append(epoch)
                epoch += 1
                words = line.split(" ")
                time = float(words[-1]) / 60
                cost_per_epoch += time * price_per_min
                cost.append(cost_per_epoch)
    
    return epochs, cost


def parse_log_for_acc(log_file):
    accuracies = []
    epochs = []
    epoch = 1
    with open(log_file) as file:
        for line in file:
            if "Accuracy:" in line:
                epochs.append(epoch)
                epoch += 1
                words = line.split(" ")
                acc = float(words[2][:-2])
                accuracies.append(acc)
    
    return epochs, accuracies

def parse_log_for_times(log_file):
    times = []
    epochs = []
    epoch = 1
    with open(log_file) as file:
        for line in file:
            if "took a total of" in line:
                epochs.append(epoch)
                epoch += 1
                words = line.split(" ")
                time = float(words[-1]) / 60
                times.append(time)
    
    return epochs, times

def plot_metric_on_same_graph(x_values, y_values_1, y_values_2, title, x_label, y_label):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.plot(x_values, y_values_1, label = "NVIDIA")
    ax.plot(x_values, y_values_2, label = "AMD")
    ax.legend(loc = 'upper left')
    plt.show()

def main(args):
    nvidia_log = args.nvidia_file
    dml_log = args.dml_file
    plot_title = args.plot_title
    plot_type = args.plot_type
    x_label = args.x_label
    y_label = args.y_label

    if plot_type == "cost":
        epochs, nvidia_cost = parse_log_for_cumulative_cost(nvidia_log, 2752.68)
        epochs, dml_cost = parse_log_for_cumulative_cost(dml_log, 2706.84)
        plot_metric_on_same_graph(epochs, nvidia_cost, dml_cost, plot_title, x_label, y_label)
    elif plot_type == "accuracy":
        epochs, nvidia_accs = parse_log_for_acc(nvidia_log)
        epochs, dml_accs = parse_log_for_acc(dml_log)
        plot_metric_on_same_graph(epochs, nvidia_accs, dml_accs, plot_title, x_label, y_label)
        
    elif plot_type == "compute time":
        epochs, nvidia_times = parse_log_for_times(nvidia_log)
        epochs, dml_times = parse_log_for_times(dml_log)
        plot_metric_on_same_graph(epochs, nvidia_times, dml_times, plot_title, x_label, y_label)

if __name__ == "__main__":
    args = default_argument_parser().parse_args()
    print("Command Line Args:", args)
    main(args)

