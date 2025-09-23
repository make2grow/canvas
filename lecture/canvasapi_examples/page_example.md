----

#### The Page Object

- `title` (not unique)
- `url` or `page_url` (unique page slug)
- `html_url` (full unique URL)
- `page_id` or `id` (unique internal ID)

---

#### Link to the Page

The page object has `page.html_url` with full URL, but we need only part of it. 

```html
<a title="..." 
   href="/courses/81929/pages/example-course-information-markdown" 
   data-course-type="wikiPages" 
   data-published="false">...
</a>
```

We can parse the relative page link.

```python
from urllib.parse import urlparse

full_url = page.html_url
parsed_url = urlparse(full_url)
relative_path = parsed_url.path
```

---

#### Usage