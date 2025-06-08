# Introduction

This repository performs a grep search inside a default directory or a specific one if provided.

# Installation

Copy the link of the github repository, click on add extension in the Extensions tab inside the settings of Ulauncher and paste the link over there.

# Usage

Write the keyword, by default is `grep` and the string you want to search followed by a space. If there is no more information in the query, it will perform a recursive search inside the default folder configured in the `manifest.json`.

```
grep Hello_world
```

You can specify another folder writing its absolute path after the search string followed by a space

```
grep Hello_world /home/user/scripts
```

It will print a list of the first ten results obtained with its name and the matching line. If you click enter with one of them highlighted, it will open the file.

> It is skipping binary files currently.

# Contributions

If you want to contribute, just create a PR with your code and assign me as a reviewer.