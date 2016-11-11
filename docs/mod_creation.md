# Creating a mod

## Step 1: Repository

The first step will be to select a repository to host your mod's metadata.

### Own metadata repository

When you link your Github account with EASI, a repository named `EASIMETA` will be created. By default, EASI will send all your mods' metadata to this repository, because it's yours.

The catch is that in order for your mods to be made available for download, end-users will need to add your repository to their list of repositories, which is a manual operation.

This is fine if, for example, you are the maintainer of all the skins for your organization.

This is less fine if you're not part of any organization and are releasing a HUD mod for the A-10C, in which case you would probably prefer to use the `root metadata repository`.

### EASI root metadata repository

The `root metadata repository` is the central repository of EASI, the only one that is visible by all the clients out of the box.

It's located at [https://github.com/EASIMETA/EASIMETA](https://github.com/EASIMETA/EASIMETA).

This time, the catch is that you cannot write in a repository you do not own.

What you can do, however, is make a copy of the repository, change it, and then send your changes to the owner with a message attached to it, describing your changes.

This process is called a `Pull Request`, and EASI will do it automatically for you.

#### The Pull Request

A `Pull request` is:

1. Making changes to someone else's repository
2. Asking that person to integrate your change into their repository

The disadvantage of the `Pull Request` method is that it may take some time between the moment you make your changes, and the moment the owner of the repository accepts and merge them, so your mod will not be available immediately.

## Step 2: Name

The name of your mod can be any text value of your choosing, as long as it fits the following 2 rules:

* Rule 1: the name of your mod must contain a string of four contiguous letters (case doesn't matter)
* Rule 2: the name of your mod must be unique *within the selected metadata repository*

## Step 3: Category

The category of your mod serves to describe its purpose to the end-user.

It also helps for sorting and finding mods.

## Step 4: Initial version number

A versionning scheme is needed to allow updates.

If you do not want to manage the versions yourself, it's mighty fine: leave it at the default when you create a new mod, and let EASI bump the version for you when you update your mod.

EASI is following the [Semantic Versioning 2.0.0](http://semver.org) rules for its versionning; both for EASI itself, and for the mods.

If you do want to customize the versionning of your mod, make sure you understand and follow SemVer guidelines.

!!! Note

    EASI uses `rc` as the default tag for the `prerelease` part of the SemVer; feel free to use any other one you like, though.
    
## Step 5: DCS version

To allow for compatibility check before the installation of your mod, it is strongly recommended to define which version of DCS your mod is designed to work with.
  
Defining a DCS version can be precise (e.g. `1.5.4.12345`) or fuzzy (e.g. `1.5.*`).

You can also specify that your mod should be working with any newer version of DCS by using the `+` sign at the end of the DCS version string (e.g. `1.5.4.12345+` or `1.5+`).
 
The `Pull from...` button reads the DCS version from your actual DCS installation, so you don't have to look it up yourself.

!!! Note

    The default value of `*` means that your mod is compatible with *any* version of DCS.
    
### Example table:

In the following table, the leftmost column is the DCS version string that has been given during the mod creation process, while, the header of the other columns is the current DCS version.

A checked cell means that the mod could be installed in that specific DCS installation.
    
|               	| 1.5.1.00000 	| 1.5.1.00001 	| 1.5.2.00000 	| 2.0.0.00000 	|
|---------------	|-------------	|-------------	|-------------	|-------------	|
| "1.5.1.0000"  	| x           	|             	|             	|             	|
| "1.5.1.0000+" 	| x           	| x           	| x           	| x           	|
| "1.5.1.*"     	| x           	| x           	|             	|             	|
| "1.5+"        	| x           	| x           	| x           	| x           	|
| "1.5.*"       	| x           	| x           	| x           	|             	|
| "1.5.2+"      	|             	|             	| x           	| x           	|
| "*"           	| x           	| x           	| x           	| x           	|
| "2+"          	|             	|             	|             	| x           	|

## Going deeper

### Directories

#### The cache

The cache is where EASI stores every local file it works with, be it texture files from mods you've downloaded or meta-data related to available mods.

By default, i'ts located in a `./cache` folder in the same directory EASI's installed in.

As it can grow quite large, you can move the cache to another location via the `Settings` menu.

##### `meta` folder

The `meta` folder contains the `metadata` of all mods.

Metadata
:   Merriam-Webster defines the term "metadata" as "data that provides information about other data". In the context of EASI, the primary "data" would be the mod itself: the textures, the *.lua files, the readme, etc. The "metadata" would be the file that contains the mod name, the list of files to download, and where to install them.

All `metadata` files are stored in a [Git][git] repository.

During normal use, you don't need to worry about it at all (except for accepting or rejecting changes to your mods).

However, nothing prevents you from [managing your repositories yourself](#managing-your-repositories).

The `metadata` inside the `meta` folder is contained within Git repositories arranged by their Github username.

##### `EASI_META`

Main EASI metadata folder

##### Custom `metarepo`


#### Managing your repositories

##### I know Git

If you're familiar with [Git](https://git-scm.com), this is the basic workflow:

1. Pull or fork the `metarepo` you want to edit
2. Make your changes
3. Commit and push / make a PR
4. Profit!

##### What's Git ?

If you're not familiar with Git but would still want to give it a try, I strongly recommend you give this a go first:

[https://try.github.io](https://try.github.io)

###### Tutorials about Git

[https://git-scm.com/docs/gittutorial](https://git-scm.com/docs/gittutorial)

[https://www.atlassian.com/git/tutorials/](https://www.atlassian.com/git/tutorials/)

###### Install Git

You will need to [download and install git](https://git-scm.com/download/win) on your machine before you can use it locally.

###### (optional) Get a GUI

Also, for the day-to-day use, you might want to use an application with a GUI instead of the crude CLI that comes with Git.

I would recommend you give [SmartGit](http://www.syntevo.com/smartgit) or [GitKraken](https://www.gitkraken.com) a go, they're both free for non-commercial use.
