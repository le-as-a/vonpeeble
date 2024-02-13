# Von Peeble
The data used for this project has been kept private due to copyright. The intent of this discord bot is to provide users with a platform to create a character for the tabletop RPG called BREAK!! RPG and allow users to make "dice rolls" via means of the bot. It uses SQLite 3 to store character information and the bot itself is written with Pycord AKA Python.

## Create function
- use `/create` to start the character creation process
- walks user through the process of creating a character for BREAK!! RPG
- provides descriptions for each part
- presents user with options for callings (classes) and species available

<img src="https://github.com/le-as-a/vonpeeble/assets/89109803/e40d1ce2-bbe3-42fa-916b-638de7af1730" width="300" />
<img src="https://github.com/le-as-a/vonpeeble/assets/89109803/85f79735-d7d2-4995-ae77-2762a7316555" width="400" />

- gives user an error if they try to type anything not between 1-10 for the rank (level)

<img src="https://github.com/le-as-a/vonpeeble/assets/89109803/b375ccee-f05d-4411-8059-de4234899d5c" />

## Check function
- use `/check` to initiate a roll

![image](https://github.com/le-as-a/vonpeeble/assets/89109803/cac8d072-1dc0-4c05-9aaf-a440628975d5)

- prompts user to select which aptitude they want to roll for
- optional settings include a reroll or adding a bonus to their end total

![image](https://github.com/le-as-a/vonpeeble/assets/89109803/62b4d6aa-67d8-4d5c-86a6-57520f34db03)

- generates a number (or two) depending on the settings user inputs
- gets the selected aptitude score from character and compares number generated to that score
- Announces the result of the check (note: user must roll at or lower than their aptitude score

![image](https://github.com/le-as-a/vonpeeble/assets/89109803/058ee296-49ff-4584-afd4-0eb201285fed)

## Rankup function
- use `/rankup` to initiate ranking your character up
- shows character's current stats for that level and what their scores will be when they rank up, asking user to confirm the rank up

![image](https://github.com/le-as-a/vonpeeble/assets/89109803/b2e38665-3285-4caa-9c65-b213749082c0)

- has a timeout of 10 seconds after which with no response cancels the rankup
- also disables the "confirm rankup" button

![image](https://github.com/le-as-a/vonpeeble/assets/89109803/08651ee6-7f2d-4c93-9b61-613340369838)

## Graveyard function
- use `/graveyard` to list the characters that have died
- users will be prompted to give a reason when deleting their character

![image](https://github.com/le-as-a/vonpeeble/assets/89109803/55b71631-c95f-43a0-8f4d-02f6bddf052d)

- if user selects "Character died." and confirms the delete, that character is added to the graveyard
- generates current datetime from when the character was deleted

![image](https://github.com/le-as-a/vonpeeble/assets/89109803/e1424b8e-7548-47f3-9dec-199229e1eff5)

- discord has a timestamp syntax that uses epoch unix timestamps, so we have to translate the datetime to epoch
- `new_death(user_id, char_name, calling, rank, img)` generates a datetime string and returns that when called
```
time_of_death = str(datetime.now())
time_of_death += "-0600"
```
- the time_of_death datetime string is then converted to a datetime object
- which is then converted to epoch (time.mktime() converts to your local time)
```
time_of_death = new_death(self.user_id, self.char_name, self.calling, self.rank, self.img)
dt_obj = datetime.strptime(time_of_death, f'%Y-%m-%d %H:%M:%S.%f%z')
epoch = time.mktime(dt_obj.timetuple())
```
- epoch returns a float but discord's syntax will only take an int so it must be converted
- this is then put into discord's syntax: `f"{char_name} died \n<t:{int(epoch)}:D>"`

### Other Features
- `/edit` can change the name or image of the character's profile
- `/attack` generates a number from 1-20, allows for reroll and bonus options
- `/profile` can view your character information
- `/delete` prompts user to delete their character, asks them to confirm or cancel and has a timeout feature that will disable the buttons and cancel the procedure

### Planned in the Future
- `/info` with data from BREAK!! RPG so users can look up and view abilities for their calling
