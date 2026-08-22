# d5c

My personal blog: https://humanshell.github.io — Jekyll on GitHub Pages.

## Preview locally

Requires Ruby 3.x (rbenv) + bundler.

    bundle install
    bundle exec jekyll serve

Open http://localhost:4000. Files in `_drafts/` appear here but are never published.

## Publish a post

1. Start a draft:

        ./scripts/newdraft "Your Post Title"

   This creates `_drafts/your-post-title.markdown` with front matter ready to fill in.
2. Write markdown below the front matter (`category:` and `tags: []` are optional).
3. Preview with `bundle exec jekyll serve` — drafts show locally but are never published.
4. When ready, move it into `_posts/` with a date prefix:

        git mv _drafts/your-post-title.markdown _posts/2026-08-22-your-post-title.markdown

5. Commit and push to `master`. GitHub Pages rebuilds automatically (~1 min).

## Notes

- Homepage paginates 10 posts/page (`paginate: 10` in `_config.yml`).
- Categories link to archive pages (`/poetry/`, `/programming/`, etc.) defined by the root-level HTML files.
- The tag cloud in the sidebar links into `/tags/`, which lists every tag with its posts.
- RSS feed lives at `/feed.xml`.
- The `github-pages` gem in the Gemfile pins the local build to exactly what Pages runs — if `bundle exec jekyll build` passes locally, the deploy will pass.
