# SharePoint-Online Deployer

A very simple script that helps to create a `sppkg` package to deploy a sharepoint online solution.

In particular this script does:
- optionally update/change the version of the solution
- run the commands to create the package (any parameter will be passed to those commands):
	- `gulp clean [args...]`
	- `gulp bundle --ship [args...]`
	- `gulp package-solution --ship [args...]`
- optionally commit the new version
	(it adds only the `config/package-solution.json` file)

**You must be in the root of your project** since it uses the work directory instead get the folder as input (I told you that it's a very simple script).


### Example of usage

```bash
$ deploy --env cluster # the "--env cluster" will be passed to all the gulp commands, normally you don't have to pass any
Update the version? 1.0.0.0 -> 1.0.0.1 [Y/n/x.y.z.k] y # here you can also specify the version you want, like 1.2.3.4
Solution version: 1.0.0.1
<... gulp stuff ...>
commit the new version? [Y/n] y
[branch de4db33f] "version 1.0.0.1"
<... others git stuff ...>
```
after that the package should be placed in `sharepoint/solution/<solution_name>.sppkg`


> NB: it's actually pretty simple adding some behavior, for example open the folder where the package was created and the browser at the AppCatalog page to deploy it.
> Anyway in the code there is a comment that suggest where to place some custom behavior.

