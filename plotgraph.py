
import matplotlib.pyplot as plt

# Model names and accuracies
models = ['KNN', 'Logistic Regression', 'Random Forest', 'SVC', 'GDB']
accuracies = [88.46, 87.18, 83.97, 91.03, 98.99]

# Plotting the accuracies as a line plot with scatter points
plt.figure(figsize=(10, 6))
plt.plot(models, accuracies, color='red')
# Plot the accuracies as scatter points
plt.scatter(models, accuracies, color='black', marker='o', s=50, label='Accuracy')

# Draw dotted lines from each point to the x-axis
for model, accuracy in zip(models, accuracies):
    plt.plot([model, model], [0, accuracy], linestyle=':', color='gray', linewidth=1)

# Add labels and title

plt.title('Model Accuracies with Connection to X-axis')
plt.xlabel('Model')
plt.ylabel('Accuracy (%)')

# Annotate each point with its accuracy value
for model, accuracy in zip(models, accuracies):
    plt.annotate(f'{accuracy:.2f}%', (model, accuracy), textcoords="offset points", xytext=(0,10), ha='center')

plt.ylim(0, 105)  # Set y-axis limit from 0 to slightly above max accuracy for padding
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility

plt.legend()
plt.show()
