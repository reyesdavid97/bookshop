# Bookmart

To run, make sure you have python and django installed. Then run the database migrations with
```
python manage.py migrate
```
and then serve the application with
```
python manage.py runserver
```

The app should be running at `http://127.0.0.1:8000/`

---
### Seeding books

There's a fixture included with some books to seed the database when it's empty. It's always growing. To load it 
run the following 
```
python manage.py loaddata book_seed.json
```

If you add more books and want to update the book seed you can do the following
```
python manage.py dumpdata books > book_seed.json
```
Note that this will override the current seed with whatever your db has. Also make make sure that your book covers are either urls pointed to images in the `static/covers` directory, or are remote urls. 