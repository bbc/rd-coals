# Semantic Versioning

This project uses a slightly refined iteration of [semantic version][SEMVER] - aka "SEMVER"
This is derived from usage on a handful of previous projects, and it seems
to work well for signposting specific changes - especially with regard to
development releases. 

##  What is SEMVER and why the change? 

In semantic version 2.0.0, the version number of the project has the format
MAJOR.MINOR.PATCH where each element is a number.

These change as follows:

* MAJOR - When the "project API" change in a non-backwards compatible manner
* MINOR - When functionality changes in a backwards compatible manner
* PATCH - When functionality is fixed/minor improvements in a backwards compatible manner. 

How to track developer releases, and similar isn't addressed by this.
Similarly, given "enough" PATCH releases, these can realistically amount
to a feature change/improvement. For example, if you have 10 performance
related bug fixes, collated together that's a feature change.

##  Semantic Versioning with development releases

Traditionally a version number 0.X.Y means "this is under development, beware".
A version number of W.X.Y where W >= 1 means "this is a stable release.

The question is how to track this - and how to track the relationship between
development and release.

The solution taken here is as follows:

### STABLE release:

* MAJOR >= 1 - increases when the "project API" change in a non-backwards compatible manner
* MINOR - increases with new features in a backwards compatible manner
* PATCH - increases when functionality is fixed/minor improvements in a backwards compatible manner. 

### DEVELOPMENT release:

* MAJOR == 0 - Never increases.
* MINOR - increases with new features (Whether backwards compatible of not)
* PATCH - increases when functionality is fixed/minor improvements in a backwards compatible manner. 

No number for either style of release ever goes back down to zero. MINOR and PATCH are incremented across both styles of release.

## Example release log

* 0.0.1 - First experimental release
* 0.1.2 - Bug fix
* 0.1.3 - Performance
* 1.1.4 - Declaration of a first stable API
* 1.1.5 - Bug fix
* 1.2.6 - New backwards compatible feature
* 0.2.7 - Experimental changes to stable release
* 0.3.8 - New experimental feature
* 0.4.9 - Another new experimental feature, not backwards compatible.
* 2.4.10 - New stable release. The not backwards compatible nature forces MAJOR revision update

### Stable Releases

This means the stable release history looks like this:

* 1.1.4 - Declaration of a first stable API
* 1.1.5 - Bug fix
* 1.2.6 - New backwards compatible feature
* 2.4.10 - New stable release. The not backwards compatible nature forces MAJOR revision update

### Development Releases

The development history looks like this:

* 0.0.1 - First experimental release
* 0.1.2 - Bug fix
* 0.1.3 - Performance
* 0.2.7 - Experimental changes to stable release
* 0.3.8 - New experimental feature
* 0.4.9 - Another new experimental feature, not backwards compatible.

This allows packages that depend on the stable releases to pick a version >=1.
Those that are doing development can still use packages, but depend on versions < 1.
However there remains at all times clear chronology.

It also means the project can never have a version 1.0.0, 2.0.0, etc.


[SEMVER]: https://semver.org
