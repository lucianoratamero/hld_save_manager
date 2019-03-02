# hld_save_manager

This project **tries** to implement a save/load state feature for Hyper Light Drifter.

## Usage

Download the [current exe file](./raw/master/dist/hld_save_manager.exe) and open it.

### Creating save states

If you have a save in a point you want to use as a save state, click on *Create save state*, select the file and give it a name.

The registered save states are saved in the '''/hld_save_manager/saves/''' folder, together with your binding configurations.

### Preparing to load save states on save slots

To prepare a save state to be loaded into a save slot, click on the '''Set save for slot''' button for the slot you will want to use it in.

This does **not** put the save in the slot, it only sets up everything to do that.

It is preferrable for you to use it together with the **Create save state from save** feature, so you have everything backed up.

### Loading the save state into the slot

To load a state, you may press one of the following keybindings:

- 'ctrl+shift+z' for slot 0 (the first one)
- 'ctrl+shift+x' for slot 1
- 'ctrl+shift+c' for slot 2
- 'ctrl+shift+v' for slot 3 (the last one)

**THIS WILL OVERWRITE THE SAVE FILE FOR THAT SLOT**

Be sure to save a new state for save files you want to keep **before** using this feature.

**Note:** if you're at the main menu when you press the keybindings, the game will not catch up with the data and will show the wrong details when you try to load it. Don't worry: the data is there, so if you load the game, it will load your state properly. If there wasn't a save in that slot previously, you may need to restart the game.
