# Microformats Python Parser Website

Website for Microformats Python parser (based on pin13.net by [@aaronpk](https://github.com/aaronpk)).

https://python.microformats.io

## Deployment

All commits to the `master` branch get auto-deployed to the live website (running on [Heroku](https://python.microformats.io))

## Getting Started

This website is built using Python Flask.

To start working with this project, first clone the repository for this project:

```
git clone https://github.com/indieweb/microformats-python-parser-website.git
cd microformats-python-parser-website
```

Next, install the required dependencies:

```
pip3 install -r requirements.txt
```

Next, start the server. You can do this in either debugging mode (where `debug=True`) in Flask or in production mode using Gunicorn.

```
python3 app.py --debug (debug mode)
gunicorn app:app (production mode)
```

You can view your running local application at this URL:

```
http://localhost:8080
```

## Requirements

- Python 3.9

## Contributions

1. Fork it
2. Get it running (see Installation above)
3. Create your feature branch (`git checkout -b my-new-feature`)
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin my-new-feature`)
6. Create new Pull Request

If you find bugs, have feature requests or questions, please
[file an issue](https://github.com/indieweb/microformats-parser-website-python/issues).

## License

Microformats Python Parser Website is dedicated to the public domain using Creative Commons -- CC0 1.0 Universal.

http://creativecommons.org/publicdomain/zero/1.0

## Contributors

- Kyle Mahan / [@kylewm](https://github.com/kylewm) (Author)
- [@capjamesg](https://github.com/capjamesg) (Contributor)