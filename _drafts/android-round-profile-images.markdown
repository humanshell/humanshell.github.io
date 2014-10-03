---
layout: post
title: Android Round Profile Images
---

I just ran into a similar issue while trying to display round (circular) profile images in my first Android app. I am also using Universal Image Loader and I display user profile avatars in a few locations right now but they only display **in two different sizes**. On the main profile activity the user's avatar is in a 100dp square `ImageView` like this:

    <ImageView
        android:id="@+id/avatar"
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:layout_alignParentTop="true"
        android:layout_alignParentLeft="true"
        android:layout_alignParentStart="false"
        android:contentDescription="@string/profile_avatar"
        android:layout_marginLeft="30dp"
        android:layout_marginTop="10dp"
        android:layout_marginRight="10dp" />

On other pages where I need to attribute the content to the user that created it I use a smaller 50dp square `ImageView` like this:

    <ImageView
        android:id="@+id/avatar"
        android:layout_width="50dp"
        android:layout_height="50dp"
        android:layout_alignParentTop="true"
        android:layout_alignParentLeft="true"
        android:layout_alignParentStart="false"
        android:contentDescription="@string/profile_avatar"
        android:layout_margin="10dp" />

As I said above, I wanted these images to be displayed as circles to differentiate them from other images being displayed in the activity. The problem I ran into was that either the image was too small and would appear in the upper left-hand corner and then stretch the pixels out along the rest of the canvas that UIL is drawing, or the image displayed too large so it appeared as though the circle was cropping out most of my image.

I tried to read the UIL code in `RoundedBitmapDisplayer` but it's still a little over my head. Instead I just kept experimenting with different image sizes until I found the dimensions that fit without a need for UIL to scale inside the canvas.

What really saved me is that I am using [Gravatar][1] for my app's avatars. So I can ask Gravatar for whatever size I want by passing query params in the request. Here's what I ended up doing:

1.) I defined a static method on an application class I've been using to collect general util methods. I need this method because I'm getting my Gravatar URLs from my Rails API.

    public static String rebuildAvatarUrl(String url, String size) throws URISyntaxException {
        URI uri = new URI(url);
        return "https://" + uri.getHost() + uri.getPath() + "?s=" + size + "&d=identicon";
    }

2.) I can pass in the URL I get from the `AsyncTask()` that talks to my API and get back a well formed Gravatar URL when loading up my `ProfileActivity`. So in my activity I call this:

        try {
            String imageUrl = MyApp.rebuildAvatarUrl(prefs.getString("avatar_url", null), "300");
            ImageLoader.getInstance().displayImage(imageUrl, avatarView, MyApp.avatarUILOptions(200));
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }

Now the trick I figured out is that you need very specific dimensions when asking UIL to draw these circular canvases. Basically it comes down to this:

1. if you want a perfect circle pass a radius to `RoundedBitmapDisplayer` that is **two times** the size of your image. In my example above I pass a radius of 200. This means the image I'm loading is my first example from above. It's the avatar I display on the main `ProfileActivity` for the logged in user on my app.

2. the actual size of the image needs to be **three times** as large as the `ImageView` in which you are going to display it. If you look back at my XML you'll see that I am using a 100dp square `ImageView` so my image needs to be 300px.

For the sake of completeness here is the second static application class method from above so you can see how I am configuring my UIL DisplayOptions:

    public static DisplayImageOptions avatarUILOptions(int radius) {
        DisplayImageOptions.Builder options = new DisplayImageOptions.Builder();
        options.showImageOnLoading(R.drawable.blank_image);
        options.cacheInMemory(true);
        options.cacheOnDisc(true);
        options.displayer(new RoundedBitmapDisplayer(radius, 0));
        options.bitmapConfig(Bitmap.Config.RGB_565);
        return options.build();
    }

I hope this helps someone, I realize that if you are getting images in a fixed size my solution may not help. But if you do have access to an API or service where you can ask for a specific size this could solve your UIL stretch image problems.



  [1]: http://en.gravatar.com