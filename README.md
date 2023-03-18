# Server files
Instructions coming soon:tm:.

Rough instructions:
- Download Smartfox Server Pro 1.6.6 (commonly shortened to SFS Pro) from its official website.
- Extract it twice to two folders called `sf-notification` and `sf-game` (make sure it doesn't have an SFS_1.6.6 folder in it, extract the contents of SFS_1.6.6 folder into these two folders) .
- Copy the contents `sf-notification` and `sf-game` files into the extracted files respectively. Replace if necessary.
- Set up a MySQL server via any method, XAMPP can help simplify on Windows.
- Create a database called `shso`.
- Use the provided `.sql` file for a sample DB with username: `User` and password: `password` (simply excute it in your MySQL server).
- Edit the `config.xml` file in both folders and provide the DB's username and password, for XAMPP defaults are username: `root` and password is blank, don't put anything for the password, leave it empty.
- Edit all `sf-game/` and `sf-notification/` paths across all scripts to point to the absolute path (like, `/home/user/sf-game/` for Linux and `D:\folder\sf-game\` for Windows.
- Start the server by running a terminal window in both folders and type `.\start.sh` (for Linux, for Windows it is `.\start.bat`, don't forget to `cd` to the folder in both cases).
` Don't forget to edit the IP in the game's `AssetBundles\Configuration\server.xml`.
# Contributors:
#### Developers:
* CrabFu (Former project lead).
* FireAndIce (Former project lead).
* Omar (Ultimate Squad).
* Undisclosed contributor.
* DarkRedTitan (Mostafa Abdelbrr) (Current project leader).
* Undisclosed contributor.
* Gmjjr (Mark Jones).
#### Asset contributors:
* Undisclosed contributor.
* Remy.
* Strad.

Sincere thanks to all of the remakes of this project, as well as the community!
