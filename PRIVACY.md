# Open Source Privacy Principles

The BBC privacy policy can be found here:

* <https://www.bbc.co.uk/usingthebbc/privacy/>

In the unlikely event of a conflict between that document and this one,
the above document takes precedence.

The purpose of this document is to discuss what privacy means in the context
of open source. It also discusses and what principles we use to apply the BBC
policy in an open source context.


## 1.  Introduction

You have the right to be informed what, how, and why, your data will be
processed.  That is the purpose of this document.

The responsibility for ensuring this privacy is implemented is the data
controller.  In this case the data controller is the project originators -
The British Broadcasting Corporation.



### 1.1 I'm a developer/user just using your code, does this affect me?

**NOTE: In the vast majority of cases, we do not gather any user data.**

To be clear what this means:

    if you_are_contributing_back:
        We gather limited personal data to make this happen
    else:
        We do not gather personal data


### 1.2 This project is open source

This is an open source project.  Open source is a widely used term.  In
software, we use the definition provided by the [Open Source Initiative][OSI].
This project is licensed under the Apache 2 license.

**In the vast majority of cases, we do not gather any user data.**

We do have access to some very limited stats gathered by github.  This data
is aggregate and not personal.

When we accept contributions, we collect necessary personal data in order to accept them.

For small contributions,  we accept contributions under clause 5 of the
[Apache 2 license][APACHE2].  That is you provide us with an Apache 2
license for your code.  For larger contributions, we ask for a contributor
license agreement.  For more details, seeing CONTRIBUTING.md


### 1.3 CUSTOMARY uses of Personal Data by Open Source projects

You may be new to open source.  Even if you're not, it is useful to briefly
discuss common customs and their origins.  To see how/whether these customs
apply to this project, see Section 2.

Most projects don't use a contributor license agreement (CLA) and just rely
on standard open source licensing.  Projects that use a CLA tend to ask for
more information.

#### 1.3.1 Projects without a (CLA)

What personal data do we mean here?

Most open source projects do not track any personal data.  A major exception
is that of contributors.  This normally boils down to your name and email
address.  (Though the basic contact details could include
twitter/facebook/github handles/etc)

How do many open source projects customarily use this data?

**Authors File**

Both tend to be included in a AUTHORS file.  The reason for this is twofold,
but boils down to maintaining copyright notices:

* Your name is required in order to comply with the licensing agreements.
  Some authors go by pen names.  What your name is and what you call
  yourself is not our job to regulate.  After all, some countries have
  assumptions about a legal name, others do not.  We do NOT make any
  [assumptions about naming][NAMING].  There is an obvious exception
  there - we expect we can write it in unicode.  If we can't we'll
  find a way to credit you appropriately.

* Your basic contact details (eg email) tends to be included.  The reasons
  for this are lost in the mists of time.  In practical terms most people
  expect it these days because:
   - It helps differentiate between all the John Smiths (for example) in
     the world
   - It allows someone to get in contact with the project's contributors
     (you may/may not object to this)
   - People add it in themselves
   - It's a way of giving credit where credit is due
   - Bragging rights
   - Because it's always there
   - Because when things fail knowing who to ask what the hidden
     assumptions the code make are is important.
   - So that someone who forks the code can continue to ensure they're
     crediting people and complying with the license.

**Needing the name you want us to credit you with is the important detail.** 
We don't HAVE to publicly include your basic contact details.  However,
experience has shown that leaving them out has upset Contributors.

There are some people who simply cannot share that information publicly. 
(eg those with stalkers) If you fall into this category, we will work with
you with regard to this.

**Version Control Logs**

The other location is slightly less obvious.  Most projects use some form of
version control.  This project uses `git`. `git` - records limited pieces of
personal data in every commit that you make.  This data is:

* Author - name and email address
* Committer - name and email address.

Making your code open source means pushing your changes to a public
repository.  Those pieces of information are publicly available.  Most
projects that use github do not make any effort to withhold this
information.  The reason for this is because it allows you to identify
[who changed a particular line of code, when, how and why][GITWHODIDWHATWHEN]. 
This is particularly useful when debugging code.

Bear in mind: this can be avoided if there's a problem.  Get in touch BEFORE
you push if you need assistance on this.

#### 1.3.2 Projects with a contributor license agreement

A Contributor License Agreement is a formal agreement regarding
contributions.

There are two main types of motivation with regard to these.  They either
aim to:

* Protect the project that is receiving the contribution.
* Protect the Contributor **and** the project

This project uses a CLA of the second kind.

Furthermore, there are two kinds of CLA.

* Those that assign copyright of the code to the project "owner"
* Those that grant a highly permissive license to the project "owner" giving
  them effectively the same (or close to the same) rights over the
  contribution as the contributor

The former tends to be used by US based companies or projects.
The latter tends to be used by European companies or projects.
(Again, this project uses the second kind)

This is in part due to differences in traditions and detals around copyright law.

The latter is also useful to accept contributions from individuals
where local laws/policies make copyright is not possible/practical.

Both of those kinds of CLA tend to require the following personal information:

* Name (as per the 1.3.1 above)
* Basic contact details (as per 1.3.2 above)
* Physical contact details.  This normally an address, sometimes phone
  number.  This is so that that a signed agreement can be sent out and
  discussed if necessary

A contributor also warrants that they have the necessary authority/etc
regarding their contribution/etc.  Each CLA also tends to have lots of other
details, but these are the key ones.

Name and basic contact details tend to be used by the project as per 1.3.1

The physical contact details are used primarily for admin relating to the
CLA.  These details are **NEVER** made public.  The assumption is that they
are stored securely.  However, most CLA's do not include a privacy notice to
this effect.

In the absence of a privacy notice, any usage falls back onto standard data
protection best practice with regarding to copyright legal requirements for
the jurisdiction in which the CLA applies...


## 2. Summary of usage of Contributor Personal Data by this project

(For definitions of small and larger changes see CONTRIBUTING.md)

### 2.1 Contribution related privacy issues

For *small changes* we follow the customs for projects that don't use a CLA
(ala 1.3.1).  We **CAN** accept changes under Clause 5 of the Apache 2
license.  This means we will need to make your name public.  This would
normally also mean making your basic contact details public (one of
email/twitter/etc - your choice).  We'd check we have your explicit
permission before doing so.

For *larger changes* we use a CLA and follow those customs of projects.  We
**do not** ask for copyright assignment.  We do ask you to warrant the
changes are yours.  We would need to make your name public. This would
normally also mean making your basic contact details public (one of
email/twitter/etc - your choice).  We'd check we have your explicit
permission before doing so.

If you provide a series of small changes amounting to a large change we may
ask you for a CLA.  This is to protect you as much as us.

For changes provided by **companies** , we will **always** require a CLA.

**CLAs are done using paper.**

The paper copies are stored in secure locked storage, with limited access. 
The reason for preferring paper is specifically because it **cannot** be
electronically leaked.

However, copyright subsists a long time.  At some point it may be archived
for long term storage.  This may well mean in an electronic form.  If this
is done, the CLA will be kept in secured storage in line with industry best
practice.



### 2.2 "I can't have anything relating to me public"

**We believe this should not be a barrier to contribution.**

We know all too well that there are many reasons for asking this.  For
example - stalking exists and this should not be a barrier to contribution. 
Another might be you as a contributor live in a country where linking
publicly your details to a contribution could put you at risk. There 
can be other, less dramatic, very valid reasons.

**NOTE WELL**: If you do not wish your name/contact details to be made
public in any shape or form, we can find a way of doing this.  We can
allocate a pen name, and store contact details separately.  (And kept secure
as per the 2.1)



### 2.3 Legal basis for processing

Please see the BBC privacy policy referred to at the beginning of the document
for this sort of detail.

Fundamentally, the purpose for processing personal data is purely practical.
It enables the all the legal and practical processes that make the open source
process to work.  It also enables us to comply with our legal obligations
in doing so.

**PLEASE NOTE:**

Due to the way the public version control systems work.  Once published,
public version control history is considered immutable.  That's the whole
point of version control after all.

We are acutely aware that some people may need to revisit privacy at a later
point in time, sometimes for personal safety reasons. This can sometimes
conflict with this immutable nature of git version control. If this occurs,
please get in contact and we will take all reasonable steps that we can. 

Please note: a git repository by its nature is designed to be cloned,
duplicated, and so on.  This leads to no single repository being a "prime"
repository.  We could change our copy of the data we could not warrant to
change all repositories.



### 2.3.1 Consent?

If you actively contribute code, data and personal data, this is licensed
under separate terms - either the Apache 2 license or a CLA. We therefore
do not use consent as a basis for processing.  However, we will
check you know how we plan to use it before accepting it.

If you are not happy with this, we cannot accept your contribution.  There
may be other reasons for not accepting it after all too.

The reason for this in large part is because your code, data, name and basic
contact details (if included) would be going into a public version control
repository.  Once published it cannot be un-published.

We could potentially rewrite *our* version control instance However to do so
is extremely destructive, and highly disruptive We would seek to avoid that
in *almost* all cases.

As noted in 2.2 we know that the needs for privacy can and do change.  If
there's an issue of **any** kind, please talk to us.  Your safety is more
important than a bit of inconvenience.


### 2.3.2 Deletion

In many circumstances you have the "right to be forgotten". This isn't
absolute - since we would still need to retain licensing information.
This can include the public copyright notices. (This is partly why we
use an AUTHORS file since it makes managing such changes simpler)

If you want your details removed, we would in the first instance seek
to JUST remove them from the current published version of the repository.

Actually changing the *history* of a repository is a **massively** destructive
change on the repository. Also, as noted, any other forks (owned by others)
of the project would contain the same information - which we could not
change. As a result, it would not be reasonable to change the history,
in MOST circumstances.

That said, our intention here is to be a good actor with regard to privacy
so if you have an issue, please get in touch.

Again, consider that all forks that have been made since publication of the
code base will **also** contain the information.  We would have no authority
nor ability to change those.



### 2.3.3 Mistakes / Corrections

If we have any errors regarding your personal data, please contact us and we
will correct this immediately.  That said, remember all any personal data
included would only be data that you personally volunteer.

We would in the first instance check that it is sufficient to just correct
this in the most recent release.  If it isn't then we can discuss an
appropriate way forward.



### 2.3.4 Retention of data

Retention of data is governed by the need to do so.  We would retain a log
of deletion.  The log would be stored in the same form as CLAs.  An electronic
log **may** also be kept containing just the name.  This would be in secured
storage.  This is so that we can ensure the details do not become public.

CLA agreements would be retained as long as legally necessary - indefinitely
in practice.  At some point it may be archived for long term storage.
This may well mean in an electronic form.  If this is done, the CLA will
be stored in line with industry best practice.


### 2.3.5 Other rights

You also have a number of other rights regarding your data.

* You always have access to the publicly held data.  If you need assistance
  in accessing it we would be happy to help.

  The only privately held data would be that held in a CLA.  In the
  circumstance that you want access to that we would seek confirmation of
  your identity before releasing it - so that we release it only to the
  correct individual.  This identity check would follow
  [ICO best practice][IDCHECK] regarding this.

* You may seek to restrict processing of your personal data, should the
  circumstances arise.  We would initially remove your data from the current
  version of the project and push the new version to a public repository
  without your data.  We would then seek to resolve whatever the issue was
  that led to your need to restrict processing.

  *The circumstances under which you can restrict processing are very*
  *specific,* but quite sensible.  Please read the Information Commissioner's
  Office's description of the rights and circumstances regarding
  [restricting processing][RESTRICTPROCESSING].  It's better than a summary
  would be here.

* You have the right to data portability.  This is built into the
  distributed nature of git.  You don't need us to continue to work on,
  develop and share your code.

* You can [object to how we use data][RIGHTOBJECT].  We will seek to always
  comply where practical, reasonable or where we must do so.  If we cannot
  comply without removing your data from our public repositories we would
  seek to make changes as per 2.3.3.  If that is insufficient, we would seek
  to remove your data as per 2.3.2, subject to any legal retention
  requirements 2.3.5

* We do not use any automated decision making or profiling.  If this was to
  change we will expand this section regarding [your rights regarding
  automated decisions][AUTOMATEDDECISIONS].



## 3. I forked your code, does this affect me?

This is a matter of perspective.

This project currently uses git and github for collaboration.  Since github
is outside our control.  This section is therefore for information, and the
world may change around us.

Suppose you use github's "fork project" feature.  Github will retain a link
between your fork and this project.  This means that users encountering your
fork can trace back to this project.  Specifically they follow the project's
network members link.

They will see your fork in that list.  This does mean that someone could
track back to your github account via this project.  This is not something
we control, it's just the way github works.

If you wish to avoid this, you can [duplicate the repository][DUPLICATE]
instead.  The link takes you to github's excellent instructions regarding
this.



## 4. Subject Access Requests, Disclosures and Breaches

### 4.1 Subject Access Requests

**For most users since we will hold no personal data the response will be
that we do not hold any user data.**

For contributors WITHOUT a CLA, we will:

* guide you as to where the limited data is in the public git repository.

For contributors WITH a CLA, we will:

* First guide you as to where the *limited data* is in the public git repository.
* Then [confirm your identity][IDCHECK].
* Then share with you the private data held in the CLA.

If there is a problem we will make all reasonable efforts necessary to
assist you.  Note though, the basic limited data is readily available.

### 4.2 Disclosures to others.

Disclosures to others - such as law enforcement - will be guided by BBC
standard policy on this matter.  This would under the current legal scheme
normally require a court order, warrant or similar.  This will follow ICO
best practice.  If you require the detailed policy, please get in contact.

### 4.3 Breaches

The law is very clear on what MUST be done in the event of a data
breach.  Most data provided is provided publicly, so this would not
be covered.  It would only cover private data that is stored in a
CLA (or volunteered by some other reason by the contributor).  In the
event of a data breach of that private data we would again seek to
follow [best practice with regard to breaches][DATABREACH].

Using a paper based approach, in locked storage in secure BBC premises,
is the preferred mechanism for seeking to prevent any personal data
breach.  As such a breach would only be possible if the physical storage
was accessed, or if the project data was archived electronically if that
secured storage was breached.


## 5. Question not covered?

If you have a question that is not covered by this privacy policy, please
get in touch.  We take your privacy very seriously, and are happy to discuss
things and revise this policy where necessary.

[OSI]: https://opensource.org/
[NAMING]: https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
[GITWHODIDWHATWHEN]: https://git-scm.com/docs/git-blame
[DUPLICATE]: https://help.github.com/articles/duplicating-a-repository/
[APACHE2]: https://www.apache.org/licenses/LICENSE-2.0

[IDCHECK]: https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-of-access/
[RESTRICTPROCESSING]: https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-restrict-processing/
[RIGHTOBJECT]:  https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-object/
[AUTOMATEDDECISIONS]: https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/rights-related-to-automated-decision-making-including-profiling/
[DATABREACH]: https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/personal-data-breaches/
