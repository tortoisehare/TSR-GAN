#Author: muddassir235

### Data exploration visualization goes here.
### Feel free to use as many code cells as needed.
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
# Visualizations will be shown in the notebook.
%matplotlib inline

num_x = 5
num_y = 5
fig, ax = plt.subplots(num_y,num_x)
fig.set_size_inches(10,15)
for i in range(num_x*num_y):
    n = random.random()*n_train
    ax[int(i/num_x)][i%num_x].imshow(X_train[n])
    coords = c_train[n]
    rect = patches.Rectangle((coords[0],coords[1]),coords[2]-coords[0],coords[3]-coords[1],edgecolor='#00ff00',facecolor='none')
    ax[int(i/num_x)][i%num_x].add_patch(rect)
    ax[int(i/num_x)][i%num_x].set_title(sign_names[y_train[n]], fontsize=8)

plt.show()
