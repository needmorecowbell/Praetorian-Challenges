# Praetorian Rota Challenge

<p align="center">
  <img width="383" alt="image" src="https://user-images.githubusercontent.com/7833164/70473386-eeb1b500-1a9e-11ea-8b10-ddab5dcc4280.png">
</p>

I attempted to first create a module for normal board movement with an interactive mode. This was an attempt to make the automated portion easier on myself. Once the board was created, I tried to create an interactive mode for debugging, but the quick timeout made this difficult. I had never heard of this game before, and it was an interesting challenge to intentionally stall the game into winning.

-------------------

## Installation

If you're not testing, all you need is the requests library. If you are testing, use `pip install -r requirements.txt`


## Usage

```
usage: rota_cli.py [-h] [-v] [-f] email

positional arguments:
  email          email to attach to game

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
  -f, --force    stall game to win every time
```

## Testing

Use `pytest tests/* -v` to run all current unit tests


---------------------

## Methodology


### Placement 

I broke the automation portion into 2 parts: placement, then stalling. Placement depends on whether you are the first or second to move. 

**The First Piece**

The first to place has an advantage, and I found that you must place your piece next to the opponent to avoid a loss during this phase. If the player is the first to place, I chose to arbitrarily go in the 2nd spot. 

**The Second and Third Move**

After the first move, everything is relative to the move of the opponent. 

### Stalling

 To intentionally stall, I found that moving pieces towards the center should be done only if absolutely necessary, as it often leads to a determinate ending. Keeping all pieces evenly distributed and on the outside edges is ideal.


### Threat Finding