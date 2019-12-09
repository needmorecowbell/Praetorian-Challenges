## Praetorian Rota Challenge

I attempted to first create a module for normal board movement with an interactive mode. This was an attempt to make the automated portion easier on myself. Once the board was created, I tried to create an interactive mode for debugging, but the quick timeout made this difficult. I had never heard of this game before, and it was an interesting challenge to intentionally stall the game into winning. To intentionally stall, I found that moving pieces towards the center should be done only if absolutely necessary, as it often leads to a determinate ending. Keeping all pieces evenly distributed and on the outside edges is ideal.

### Placement 

I broke the automation portion into 2 parts: placement, then stalling. Placement depends on whether you are the first or second to move. 

**The First Move**
The first player has an advantage, and I found that you must place your piece next to the opponent. If not, I chose to place my piece in the following slots: [2,4,6,8]

**The Second Move**
After the first move, everything is relative to the move of the opponent. 

### Stalling