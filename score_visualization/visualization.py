import matplotlib.pyplot as plt
import csv


def plot_a_star_score(file_name):
    x = []
    y = []

    with open('./' + file_name,'r') as file:
        lines = csv.reader(file, delimiter=',')
        for row in lines:
            if len(row) > 0:
                x.append(int(row[0]))
                y.append(int(row[1]))

    plt.plot(x, y, color = 'b',
             marker = 'o',label = "Score")

    plt.xticks(rotation = 25)
    plt.xlabel('Iteration')
    plt.ylabel('Score per iteration')
    plt.title('Score', fontsize = 20)
    plt.grid()
    plt.legend()
    plt.show()
    print(max(y))
    print(sum(y) / len(y))
    print(len([i for i in y if i > 5])/len(y))