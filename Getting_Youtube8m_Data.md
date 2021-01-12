# Getting Youtube8m Data

## Getting Video IDs

### Step 1: Category Mapping

The current working solution is as follows. Go to [Youtube8m explore](https://research.google.com/youtube8m/explore.html), and inspect the js to get the list of all entities with mapping. The same has been created as a csv file in `yt8m_categories.csv`.

### Step 2: List of video IDs

For each category above, the corresponding video ids can be accessed at

    'https://storage.googleapis.com/data.yt8m.org/2/j/v/{category_id}.js'.format(category_id)

Run the following script:

    python download_yt.py