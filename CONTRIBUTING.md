# Contributing

Thanks for wanting to improve the project!

Before contributing back, please familiarise yourself with a few things
we mention below.

## Can I contribute?

Yes.  Contributions are accepted based on the merit of the contribution,
not on the basis of who they are from.

And we do mean YOU!  This is irrespective of age, gender, religion, race
or sexuality.  If you're from any group - under or well represented,
whether you're a beginner, advanced mage, or "imposter" you're welcome. 
If you can't code, you can create examples, write docs.  Informed
opinions are welcome.

This project is fundamentally about enabling learning.  We've all learnt
things in the past, and we're all experts at learning things.  Some
people are experts in other people learning or teaching things - you're
welcome too.

Please respect each other.

## What is a contribution?

The obvious answer is code.  Be it a one line typo change, a bug fix,
feature improvement, new minor feature, major feature or complete rehaul.

However, documentation, examples, videos, blogs, vlogs, podcasts, active
examples, media, hosted versions, and testimonials of usage are all
useful contributions.  In places where we can include them with the
release that would be wonderful.  In places where that's not practical,
we'd link to you (linking isn't endorsement of content of course!).

Posting on social media of any kind with the hashtag #COALS_CORE
or #PYTHONCOALS would also make our day :-)

## Contact us!

Ideally the best time to contact us is before you start work on any
potential contribution.  The second best time is when you read this.
We might be able to save you time and effort. If we can't we might be
able to say how it fits with the wider project.

Failing that it's always great to hear from people who are interested and
using the work.

The best way to do this is to open and issue.  Please note, that where a
feature is requested, but we can't add *right now*, will result in us
adding it to a "possible features" file, with a link to the issue, and
close the issue.  Please don't take offense if we close the issue.  It
means we've listened and acknowledged it.  We will also have taken some
sort of action.  We will have either implemented it, added it to the
discussion pile, or similar.


## Accepting Contributions

For some contributions to the code/docs we need a **Contributer License Agreement**
in order to accept your contribution.  This enables us to originate the
license for the project as a whole.  This is to enable us to protect your
interests in the code, in the event that the copyright license over the
project is breached by a third party.  (We can't protect code where we
haven't originated the license)

The Contributor License Agreement we use is in the file [CLA.md](CLA.md) and is
modelled on the approach taken by the Python Software Foundation for the
main implementation of the `python` programming language.

For individuals, we can accept small changes without a CLA.  If you are
contributing on behalf of a company, we require a CLA.

Please see the [PRIVACY.md](PRIVACY.md) file for details as to what happens with
personal data in both cases.

Read on for what we mean by small and large contributions, and how we
define them relative to [semantic versioning][SEMVER] as used by this
project.


## Semantic Versioning

This project uses a refined iteration of [semantic versioning][SEMVER].

This is derived from usage on a handful of previous projects, and it
seems to work well for signposting specific changes - especially with
regard to development releases.

For development releases, the version MAJOR.MINOR.PATCH has the following
rules:

* MAJOR == 0 - Never increases.
* MINOR - increases with new features (Whether backwards compatible or not)
* PATCH - increases when functionality is fixed/minor improvements in a
  backwards compatible manner.

For stable releases, the version MAJOR.MINOR.PATCH has the following rules:

* MAJOR >= 1 - increases when the "project API" change in a non-backwards
  compatible manner
* MINOR - increases with new features in a backwards compatible manner
* PATCH - increases when functionality is fixed/minor improvements in a
  backwards compatible manner.

MINOR and PATCH always increase and are kept in sync across ALL releases. 
No version number for each release "branch" ever reverts to zero.  A
chronological history of development & stable releases could therefore
be:

* 0.0.1, 0.1.2, 0.1.3, 1.1.4, 1.1.5, 1.2.6, 0.2.7, 0.3.8, 0.4.9, 2.4.10

See [SEMVER.md](SEMVER.md) for more detail

### Small contributions

Most changes that would bump the PATCH number are considered Small
Contributions.  Some changes that bump the MINOR or MAJOR numbers can be
considered small contributions too.  (For example a feature that results
in a patch file smaller than 100 lines)

### Larger contributions

All other changes are large contributions.

If you contribute enough small changes, we may well ask you for a CLA -
in order to protect your and the project's interests over the code.

## Rejecting Contributions

We will sometimes have to reject contributions. This is a fact of life

Picking a silly example, if the project was for a fire engine, it would
be rather odd to accept a flame thrower extension to the truck.  (Unless
we'd decided to redefined Fireman as per Fahrenheit 451!)

If we reject the contribution we will let you know clearly why. We're
actually more likely to also let you know what we think would be
necessary changes in order to accept your contribution.

Either way, that doesn't stop you using your change nor stop you releasing
your version.  It just means it doesn't fit with the project as we see it
at this time.

One general exception we won't accept contributions from contributors who
are disrespectful of other contributors. Such people eventually drive away
all others, and we want to foster a space where people can contribute,
and build something useful. A welcoming environment means more voices,
and more voices means we build some more rounded.


## Proposing Changes

Please open an issue.  Then fork the project.  Make your changes in your
clone fork, and create a pull request, referencing the issue. We'll then
discuss the pull request in the issue.

We would expect code quality to be at least as good if not better than
the code quality of the project at the time you make your contribution.
After all, we all hope to leave things better than we find them!

As time progresses, this section will be more fleshed out.

---

## References:

* [PRIVACY.md](PRIVACY.md)
* [SEMVER.md](SEMVER.md) - semantic versioning tweak we use
* [CLA.md](CLA.md) - the Contributor License Agreement we use (based on python's approach)
* [Semantic Versioning][SEMVER]

[SEMVER]: https://semver.org
