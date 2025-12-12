# 🐦 Flappy Bird AI using NEAT

An AI-powered Flappy Bird game that uses **NEAT (NeuroEvolution of Augmenting Topologies)** to train neural networks through genetic algorithms. Watch as generations of birds learn to navigate through pipes autonomously!

## ✨ Features

- **Autonomous Learning**: Neural networks evolve to control bird movement
- **Real-time Visualization**: Watch birds learn with generation counter, score, and population display
- **Fitness-based Evolution**: Birds that survive longer and pass more pipes create the next generation
- **Model Persistence**: Automatically saves the best network after achieving score of 20

## 🧠 How It Works

**NEAT Algorithm** evolves both neural network weights and structure:
1. Start with 50 simple neural networks (one per bird)
2. Each bird gets fitness points: +0.1 per frame, +5 per pipe passed, -1 for collisions
3. Best performers reproduce to create the next generation with mutations

**Neural Network**: 3 inputs (bird Y position, distance to top pipe, distance to bottom pipe) → 1 output (jump if > 0.5)

## 🚀 Installation & Usage

```bash
# Clone the repository
git clone https://github.com/Ashita-Sharma/FlappyBirdAI.git
cd FlappyBirdAI

# Install dependencies
pip install pygame neat-python

# Run the game
python flappy_bird_ai.py
```

**Requirements**: 
- Python 3.7+, pygame, neat-python
- `imgs/` folder with sprites (bird1-3.png, pipe.png, base.png, bg.png)
- `config-feedforward.txt` configuration file

**Training Progress**: 
- Gen 1-10: Learning basics
- Gen 20-30: Navigating multiple pipes
- Gen 40+: Consistent high scores
- Stops automatically when score reaches 20

## ⚙️ Configuration

Create `config-feedforward.txt` with NEAT parameters. Key settings:
- `pop_size = 50` - population size
- `num_inputs = 3` - bird Y, top distance, bottom distance  
- `num_outputs = 1` - jump decision
- `fitness_threshold = 100` - training goal

[Full configuration example](https://neat-python.readthedocs.io/en/latest/config_file.html)

## 🏗️ Project Structure

```
FlappyBirdAI/
├── flappy_bird_ai.py          # Main script
├── config-feedforward.txt      # NEAT configuration
├── best.pickle                 # Saved best model
└── imgs/                       # Game sprites
```

## 🔧 Customization

**Difficulty** (in Pipe class):
```python
GAP = 200  # Pipe gap size
VEL = 10   # Pipe speed
```

**Target Score** (in main function):
```python
if score > 20:  # Change threshold
```

## 🐛 Troubleshooting

- **Missing images**: Ensure all sprites are in `imgs/` folder
- **Module not found**: `pip install neat-python pygame`
- **All birds die instantly**: Check NEAT config mutation rates

## 🎯 Future Ideas

- Difficulty levels with varying pipe speeds
- Neural network visualization
- Manual play mode vs AI
- Training statistics and graphs

## 📚 Resources

- [NEAT-Python Docs](https://neat-python.readthedocs.io/)
- [Original NEAT Paper](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Ashita-Sharma/FlappyBirdAI/issues).

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👏 Acknowledgments

- NEAT algorithm by Kenneth O. Stanley
- Flappy Bird concept by Dong Nguyen
- NEAT-Python library by CodeReclaimers

## 📧 Contact

**Ashita Sharma**
- GitHub: [@Ashita-Sharma](https://github.com/Ashita-Sharma)

---

⭐ **Star this repo if you found it helpful!** ⭐

**Happy Learning! 🎓🤖**
