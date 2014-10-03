---
layout: post
title: Deploying Ghost to Heroku
date: '2013-09-24 16:00:00'
category: programming
tags: [ghost]
comments: true
---

I just got my hands on my shiny new copy of [Ghost](https://en.ghost.org) v0.3.0! What's the first thing I wanted to do? Deploy my new personal blog to [Heroku](http://heroku.com)! In my first post on my new Ghost blog I'm going to outline the steps that were necessary for me to first get Ghost running locally and then successfully deploy the site to Heroku.

Like most of you, I've been "waiting patiently" for the first release of this new blogging platform. Each chime from Mail carried on it's melody the possibility of a new Ghost update, always wondering: is today the day? That day has finally arrived, and I couldn't wait one more minute to get a look at what the Ghost team had created for us.

## Initial Setup

According to a few posts on the [forum](https://en.ghost.org/forum/installation), some of my fellow Ghosters experienced various installation related issues. I was one of the lucky ones that experienced no problems with my install. The first version of the [Ghost installation docs](http://docs.ghost.org/installation/) did an admirable job of getting me up and running in a minimal amount of time. If you haven't read them and gotten your NPM packages installed, you should do that now. The rest of this article will make no sense if you don't.

I started inside the directory that I unzipped directly from the downloaded Ghost v0.3.0 archive. I took a few minutes to peruse the directory structure trying to take note of where some important looking files and folders existed. When I couldn't take it anymore I executed `npm start` and loaded localhost:2368 in Chrome. I entered the obligatory username and password and there it was: the interface I'd been waiting to see for almost four months. I spent some time clicking buttons, exploring the menus and changing various profile settings, but there was code to look at - so I headed over to [Sublime](http://www.sublimetext.com).

While I am not new to Javascript, I am still a newcomer to [Node](http://nodejs.org). Therefore I tried to focus on some of the more common files found in a Node based project. I reviewed `package.json` and `index.js` and then tried to familiarize myself with the content and core directories. Once I felt comfortable with the general layout of the files I poured over `config.js`. I knew there would be plenty of time in the future for digging through the core codebase, my goal at this point was to find any information that may be needed for the eventual deploy to Heroku.

The config file contained a lot of the settings I knew I'd need during my Heroku deploys. I started experimenting with the settings in the development section to see what I could safely change and what caused major problems. I updated the `url:` property to reflect the address I'd like to use for local development and changed all the `port:` properties to match (I prefer to use localhost:4000 due to development on a [Rails](http://rubyonrails.org) app using localhost:5000). The database section was going to be where I'd be spending most of my time, but we'll get back to that in a minute.

At this point I took a few minutes to create a new Heroku app so I could provision some necessary addons and setup its configuration settings to make sure it was ready to receive my first deploy when that time came. If you don't have a Heroku account, or unfamiliar with creating a Heroku app, they have [great documentation](https://devcenter.heroku.com/articles/quickstart) to get you up and running really quickly.

## Mail Configuration

The Ghost docs were once again very helpful with mail setup. Even though there is no advanced email functionality currently enabled in the Ghost core, I wanted to follow all the directions as closely as possible.

According to the Ghost docs:

>At the moment, the only thing Ghost uses email for is sending you an email with a new password if you forget yours.

The documentation recommends either Mailgun or Sendgrid. The provided example explains setting up Mailgun, but the `config.js` example code is pre-populated with Sendgrid details. I decided on the latter for no particular reason and added their starter [Heroku Addon](https://addons.heroku.com/sendgrid) to my newly created app.

To test the new settings I entered my Sendgrid details into the mail section of `config.js` and restarted the Ghost server (you always have to restart the server when you update your config settings).

{% highlight json %}
development: {
    ...
    mail: {
        transport: 'sendgrid',
        host: 'smtp.sendgrid.net',
        options: {
            service: 'Sendgrid',
            auth: {
                user: 'SENDGRID_USERNAME',
                pass: 'SENDGRID_PASSWORD'
            }
        }
    },
    ...
},
{% endhighlight %}

I logged out of my Ghost site and clicked the Forgot Password link. It asked me for my email address and not 30 seconds later I had an email in my inbox with a new randomly generated password. I was able to use that to login and change my password back to what it was before the reset.

Mail settings good to go - time to dump sqlite3.

## Setup Database

From the beginning I knew this part was going to cause me the most problems. I was not wrong. Any project with a version number of 0.3.0 is going to be missing specific information about custom configuration. It would be up to me to discover how Ghost accesses a database and then how to tell it to use a different one.

Heroku seems to be in love with [Postgres](http://www.postgresql.org) and recommends it as the default <abbr title="Relational Database Management System">RDBMS</abbr> throughout its documentation. So I figured I'd start there and see what happens.

### Postgres

Postgres v9.3 was already installed on my local machine (Mac OSX v10.8.5) from a previous project. If you don't have it installed (spoiler: I ended up using MySQL so you can skip this if you want) and you're on a Mac, you can install it through Homebrew:

{% highlight bash %}
brew install postgresql
initdb /usr/local/var/postgres -E utf8   # create a database
pg_ctl -D /usr/local/var/postgres start  # start the server
{% endhighlight %}

The above commands will install Postgres, initialize a database and then start the server so Ghost can talk to that new database. Unfortunately I have next to no experience administering a Postgres database. I tried several permutations of different configuration settings in the `database:` section of my `config.js` but nothing seemed to work. I was able to get different error messages but that's only fun for a while. I did however learn that Ghost uses the [knex NPM module](https://npmjs.org/package/knex) to communicate with its database. This knowledge didn't help me to get Postgres configured but it's nice to know incase I decide to revist Postgres configuration in the future.

At this point I was getting frustrated and wanted to see some results. So I decided to fall back on that old workhorse that I was already familiar with:

### MySQL (MariaDB)

Creating the [MariaDB](https://mariadb.org) database and configuring Ghost to talk to it progressed rapidly from this point. I made the assumption that Ghost's (or knex's) MySQL configuration couldn't be that different from the [Rails database.yml](http://stackoverflow.com/questions/5872264/correct-mysql-configuration-for-ruby-on-rails-database-yml-file) format. I ended up with the following configuration:

{% highlight json %}
development: {
    ...
    database: {
        client: 'mysql',
        connection: {
            database: 'ghost_dev',
            user: 'MYSQL_USERNAME',
            password: 'MYSQL_PASSWORD'
        },
        debug: false
    },
    ...
},
{% endhighlight %}

As the gods of fate would have it I stumbled across a [forum post](https://en.ghost.org/forum/installation/113-ghost-using-mysql) that addressed these very settings after I'd gotten it up and running, but I'm glad I found a working configuration on my own. I feel a little more comfortable with how the configuration is being used by knex inside the Ghost core. And isn't that what Open Source is all about anyway? If you're paying attention (and following links) then you've noticed that I didn't copy all of the configuration properties out of that forum post. I've done this on purpose. I'm curious about how my database will work and perform if I leave out the `charset: 'utf8'` property. So far it seems to be working fine. But if I come across any errors that can be resolved by adding that property, I'll update this post with more specific information.

### NPM Modules

To get Ghost (and knex) talking to MariaDB I needed to adjust the NPM packages defined in `package.json`. As we already know, Ghost uses [sqlite](https://sqlite.org) by default. To access a MySQL database I knew I was going to need a new NPM module that provided this functionality. A quick [search](https://npmjs.org/search?q=mysql) on the NPM site returned the [module](https://npmjs.org/package/mysql) I was going to need. But how do I tell Ghost to use this module and not the sqlite module? As I mentioned above, I'm still new to Node, so my solution may not be the best. I already knew that all module dependencies are declared in `package.json`. So I started looking for the sqlite declaration. Once I found it I replaced it with the new mysql module. But I didn't know the correct version to declare. Running the command `npm info mysql` returned a bunch of details including the latest version number. I now had the information I needed:

{% highlight json %}
"mysql": "2.0.0-alpha9",
{% endhighlight %}

I then ran `npm uninstall sqlite` and `npm install`. This removed the sqlite module and installed mysql in its place along with updating any new dependencies created by the change. I'm curous as to how future Ghost updates will handle local changes to the `package.json` file. I'm concerned that a new version will overwrite this file breaking my custom mysql configuration. For now I'll just keep an eye on how new versions are released and make sure my local file is properly merged with any newer versions.

---

Before we continue I think we should recap to ensure we're all still on the same page. Here's what I'd accomplished up to this point:

1. Downloaded Ghost and installed dependencies per the official documentation
2. Verified server runs with all default configuration
3. Created empty Heroku app
4. Configured and verified mail settings through Sendgrid
5. Successfully configured Ghost to use a MariaDB database

Now that I had Ghost running locally with all the configuration that would be needed inside a Heroku app, it was time to get my repo ready for it's first deploy.

## Heroku Config & Deploy

Developing an application that will be deployed to the Heroku platform is an interesting  process. Heroku operates very differently from a traditional shared hosting or VPS based  service. Heroku runs each application in a self-contained unit they call a [Dyno](https://devcenter.heroku.com/articles/dynos). Your app's Dyno is a compiled and segregated unit that exists inside Heroku's system as a transient instance that will be created and destroyed whenever it's started and stopped. [Hannah](https://en.ghost.org/Hannah) points out one important drawback that needs to be considered when choosing Heroku in this [forum post](https://en.ghost.org/forum/installation/69-about-heroku):

>You can setup with MySQL but be warned the Heroku file system is refreshed every so often, so you would lose any uploaded images.

If this is an issue for you I'd recommend sticking with a more traditional hosting account (i.e. Amazon EC2) until Ghost matures a little more. In order to execute your local development application in an environment that most closely mimics the Heroku environment we need to configure a few tools and files.

### The Tools

When you first setup your Heroku environment on your local machine you should have installed the [Heroku Toolbelt](https://toolbelt.heroku.com). This small collection of tools ensures you have Git, the Foreman gem and the Heroku command line client installed. The Git source control management software is necessary because Heroku uses your git repository to create a new Dyno whenever you push your changes up to their platform. The foreman gem allows you to execute your application locally in a similar manner to how your Dyno will be executed on Heroku's platform. The Heroku command line client allows access to your remote Heroku account and apps to view logs, provision addons, start and stop your applications and many other administrative tasks. To see all the available commands, run this from the root of your application:

{% highlight bash %}
heroku help
{% endhighlight %}

### .env

An application that's been deployed to Heroku relies heavily on environment variables that are made available to your Dyno by Heroku at runtime. We need a way to recreate these variables in our local environment. The foreman gem allows us to do this in two ways. First it will execute your app using the commands in a `Procfile` (discussed next) and by reading predefined environment variables in a `.env` file.

In a public project, one that might also be pushed to Github or another public git repository, your `.env` should be excluded from your repository. Your `.env` could contain private keys, secrets or credentials that are needed to run your application properly but shouldn't be accessible to the public at large. You can keep this file out of source control by running this command from the root of your project:

{% highlight bash %}
echo .env >> .gitignore
{% endhighlight %}

My blog is not going to be pushed up to any server other than my Heroku account, which is private, so this step was not necessary for me. In my local environment I only need a few environment variables. The first is the node environment in which my application will run. Ghost uses this variable to decide what configuration to load and which specific pieces of code to execute. We can tell Ghost which environment to execute by adding the variable to our `.env` file:

{% highlight bash %}
NODE_ENV=development
{% endhighlight %}

I would also like to access my Sendgrid credentials in `config.js` through environment variables. This step is necessary if you're going to push your app to a public git repository. Your `config.js` has to be included in source control, but you don't want to  hard-code your Sendgrid username and password for the whole world to see. I added two more environment variables to my `.env`:

{% highlight bash %}
SENDGRID_USERNAME=my-sendgrid-username
SENDGRID_PASSWORD=my-sendgrid-password
{% endhighlight %}

I can now access these credentials from `config.js` by editing my mail configuration section a little:

{% highlight json %}
development: {
    ...
    mail: {
        transport: 'sendgrid',
        host: 'smtp.sendgrid.net',
        options: {
            service: 'Sendgrid',
            auth: {
                user: process.env.SENDGRID_USERNAME,
                pass: process.env.SENDGRID_PASSWORD
            }
        }
    },
    ...
},
{% endhighlight %}

Again, this works because the foreman gem will read your `.env` file when you launch you app and make these variables available to your app's runtime environment through `process.env.VARIABLE_NAME`. If you are going to push your app to a public repository I would suggest creating additional variables in your `.env` for your database credentials. As my repo will not be publicly deployed, I skipped this step. For now, my local database credentials are hard-coded into my `config.js`.

### Procfile

As I mentioned above, the foreman gem will run your application by executing a command from your Procfile. This command is also the one that Heroku will execute when launching your application after each deploy. So what command should we execute? We need our Procfile to use the same command that gets executed when we run `npm start`. But what command does `npm start` execute? Ghost's `package.json` configuration defines two "scripts" that can be run with the `npm` command:

{% highlight json %}
"scripts": {
    "start": "node index",
    "test": "grunt validate --verbose"
},
{% endhighlight %}

Here we can clearly see that running `npm start` will actually execute the command `node index`. This is the information we need to correctly configure our Procfile. Because this is a simple blog that doesn't need to do much more than serve web pages, we'll create the Procfile with the appropriate command in one step:

{% highlight bash %}
echo "web: node index.js" > Procfile
{% endhighlight %}

Heroku allows you to run two different types of processes: web and worker. The web process answers HTTP requests and a worker process handles background jobs. A Ghost blog doesn't need any background workers so we don't need any `worker:` declarations, but if you'd like to learn more about them, Heroku has a great introduction [here](https://devcenter.heroku.com/articles/background-jobs-queueing).

We can now verify that our configuration is correct by launching our local development app using the foreman gem. Run this command from the root of you app:

{% highlight bash %}
foreman start
{% endhighlight %}

If you see something similar to the following output, you're good to go:

{% highlight bash %}
4:46:26 web.1      | started with pid 24188
14:46:27 web.1     | Ghost is running...
14:46:27 web.1     | Listening on 127.0.0.1:4000
14:46:27 web.1     | Url configured as: localhost:4000
14:46:27 web.1     | Ctrl+C to shut down
{% endhighlight %}

You should be able to view your app in your browser in exactly the same way as you did when you ran `npm start`.

### Heroku Environment Variables

Now that my local app was configured to access environment variables and execute in the same way Heroku was going to run it, I needed to prepare my Heroku app to provide similar environment variables and configuration. How do we tell Heroku to make environment variables available to our app's runtime environment? This is where the `heroku` command line client come in. First I needed to make sure that the proper node environment is defined as well as my Sendgrid credentials. We can set remote Heroku variables using the `heroku config:set` command:

{% highlight bash %}
heroku config:set NODE_ENV=production
heroku config:set SENDGRID_USERNAME=my-sendgrid-username
heroku config:set SENDGRID_PASSWORD=my-sendgrid-password
{% endhighlight %}

You can verify these settings by running `heroku config`. That command will output all environment variables currently set in your remote environment. Once I knew these variables would be available to my app during runtime in its Dyno I had only one more hurdle to clear: **how in the heck was I going to access a database?**

If you remember I couldn't get Postgres to work above, so I fell back on MariaDB. I now needed to provision a Heroku addon that would provide a MySQL database and then create the appropriate variables that would allow my Heroku app to access it. There is only one MySQL addon available on Heroku: [ClearDB](https://addons.heroku.com/cleardb). So I added the free "Ignite" plan which offers 10 connections and a 5 MB database. This should be fine to start with, but any serious blogger would need to upgrade rather quickly to the "Punch" plan, which costs $9.99/mo and increases your database size to 1 GB with 15 connections.

**Be warned**: Heroku makes automated deploys almost brainless but can get expensive rather quickly.

Now that I had a database provisioned and ready to access, how do I configure Ghost to talk to it? The ClearDB addon creates its own environment variable which your app can use to communicate with the DB. This new variable's name is: `CLEARDB_DATABASE_URL` and takes the following form:

{% highlight bash %}
mysql://username:password@hostname/database_name
{% endhighlight %}

I wasn't sure how advanced the knex npm module would be when it came to parsing database connection URLs so I first tried to configure my database settings in `config.js` using just this URL:

{% highlight json %}
// ### Production
// When running Ghost in the wild, use the production environment
// Configure your URL and mail settings here
production: {
    database: {
        client: 'mysql',
        connection: {
            database: process.env.CLEARDB_DATABASE_URL
        },
        debug: false
    },
},
{% endhighlight %}

This meant it was time for my first attempt at a Ghost Heroku deploy. If you're following along at home, and you haven't yet turned your app's directory into a git repo, run the following command from the root of your app:

{% highlight bash %}
git init && git add . && git commit -m "Initial Commit"
{% endhighlight %}

This will initialize a git repository, add all files and then commit them. If you didn't create your Heroku app from the command line by running `heroku create` then you'll also need to add your Heroku app's repository as a remote:

{% highlight bash %}
git remote add heroku your-apps-repo-name
{% endhighlight %}

You can get `your-apps-repo-name` from the Settings area of your Heroku Dashboard under the heading "Info". Once your app is initialized as a git repo and the proper remote has been added a Heroku deploy is as simple as running:

{% highlight bash %}
git push heroku master
{% endhighlight %}

That command pushes your local git repo up to your remote Heroku repo and kicks off Heroku's internal deploy procedures. A slug is compiled for your app and a new Dyno is initialized and launched to execute that slug and answer HTTP requests.

Unfortunately my first deploy failed and the output of running `heroku logs` returned the same database errors I received while trying to setup Postgres. Obviously my database configuration in the production section of my `config.js` was incorrect. I tried many iterations with different permutations of the database settings until I found one that worked. Here is the final configuration in the production section of my `config.js`:

{% highlight json %}
production: {
    mail: {
        transport: 'sendgrid',
        host: 'smtp.sendgrid.net',
        options: {
            service: 'Sendgrid',
            auth: {
                user: process.env.SENDGRID_USERNAME,
                pass: process.env.SENDGRID_PASSWORD
            }
        }
    },
    database: {
        client: 'mysql',
        connection: {
            database: process.env.DATABASE_NAME,
            host: process.env.DATABASE_HOST,
            user: process.env.DATABASE_USER,
            password: process.env.DATABASE_PASS
        },
        debug: false
    },
    server: {
        host: '0.0.0.0',
        port: process.env.PORT
    }
},
{% endhighlight %}

As you can see I had to parse the `CLEARDB_DATABASE_URL` into separate variables so I could pass them individually. I set the appropriate remote variables with the following commands (refer to the ClearDB example format above):

{% highlight bash %}
heroku config:set DATABASE_NAME=database_name
heroku config:set DATABASE_HOST=hostname
heroku config:set DATABASE_USER=username
heroku config:set DATABASE_PASS=password
{% endhighlight %}

As soon as I had those variables set and `config.js` setup properly Ghost loaded right up and I ran through the signup process with no issues. I had successfully configured and deployed Ghost to Heroku running on top of a MySQL database! I also updated the `server:` section to use the HOSTNAME and PORT that Heroku creates for every Dyno. I'm not sure if the `host:` property is required but the `port:` property is. Without it, you're Dyno would not know how to communicate with Heroku's router.

## Conclusion & Next Steps

After a long wait, much anticipation and a lot of trial and error, I'm rockin' a new Ghost blog on Heroku. There is still much to do. I'm excited to see what new versions will offer us as well as for the official public release on Github. For my next projects I'm going to investigate how avatars are handled internally to see if I can add support for [Gravatars](http://en.gravatar.com) if no image has been uploaded and then begin customizing the default Casper theme so I can learn how to create my own custom themes. [This forum post](https://en.ghost.org/forum/themes/17-marketplace) states that the Ghost Marketplace will eventually be opened up to us all. I look forward to submitting some open source themes for the community to use.

I hope some of you learned something new about Ghost and maybe even got your site up on Heroku with the help of this post. I'll be back with something new soon...

### Useful Links

These are just a few links I thought might be helpful with Ghost configuration or a Heroku deploy:

1. [The Ghost Guide](http://docs.ghost.org)
2. [The Ghost Forums](https://en.ghost.org/forum/)
3. [The Ghost Marketplace](http://marketplace.ghost.org)
4. [Another Ghost Heroku deploy tutorial](http://www.howtoinstallghost.com/how-to-install-ghost-on-heroku/)
