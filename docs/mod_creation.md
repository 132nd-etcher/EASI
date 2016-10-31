# Creating a mod

## Going deeper

### Directories

#### The cache

The cache is where EASI stores every local file it works with, be it texture files from mods you've downloaded or meta-data related to available mods.

By default, i'ts located in a `./cache` folder in the same directory EASI's installed in.

As it can grow quite large, you can move the cache to another location via the `Settings` menu.

##### `meta` folder

The `meta` folder contains the `metadata` of all mods.

Metadata
:   Merriam-Webster defines the term "metadata" as "data that provides information about other data"[^1]. In the context of EASI, the primary "data" would be the mod itself: the textures, the *.lua files, the readme, etc. The "metadata" would be the file that contains the mod name, the list of files to download, and where to install them.

All `metadata` files are stored in a [Git][git] repository.

During normal use, you don't need to worry about it at all (except for accepting or rejecting changes to your mods).

However, nothing prevents you from [managing your repositories yourself](#managing-your-repositories).

The `metadata` inside the `meta` folder is contained within Git repositories arranged by their Github username.

##### `EASI_META`

Main EASI metadata folder

##### Custom `metarepo`


#### Managing your repositories directly

##### I know Git

If you're familiar with [Git][git], this is the basic workflow:

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

You will need to [download and install git][gitdl] on your machine before you can use it locally.

###### (optional) Get a GUI

Also, for the day-to-day use, you might want to use an application with a GUI instead of the crude CLI that comes with Git.

I would recommend you give [SmartGit][smartgit] or [GitKraken][gitkraken] a go, they're both free for non-commercial use.


[^1]: [http://www.merriam-webster.com/dictionary/metadata](http://www.merriam-webster.com/dictionary/metadata)
[git]: https://git-scm.com/
[gitkraken]: https://www.gitkraken.com/
[smartgit]: http://www.syntevo.com/smartgit/
[gitdl]: https://git-scm.com/download/win