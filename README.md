# ArtAPI-FastAPI
- ArtCore-FastAPI is a FastAPI server that handles the service.
- It utilizes PostgreSQL and MongoDB for data storage
- It communicates with the Go core server through gRPC.

<br>

## Getting Started

To run the service, follow the instructions below:

1. Clone the repository:

```sh
git clone https://github.com/robert-min/ArtCore-FastAPI.git
```

2. Navigate to the project directory:

```sh
cd ArtCore-FastAPI
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

4. Run the server:
- add src/libs/.env

```sh
python app.py
```

<br>


## Contributing

Contributions are welcome! If you would like to contribute to ArtCore-Go, please follow these steps:

1. Fork the repository.

2. Create a new branch:

```sh
git checkout -b my-feature
```


3. Make your changes and commit them:

```sh
git commit -m "Add my feature"
```

4. Push to your forked repository:

```sh
git push origin my-feature
```

5. Open a pull request. 

<br>


[![codecov](https://codecov.io/gh/robert-min/ArtAPI-FastAPI/graph/badge.svg?token=2MUZJH61VC)](https://codecov.io/gh/robert-min/ArtAPI-FastAPI)

## code coverage Report

```
---------- coverage: platform linux, python 3.10.12-final-0 ----------
Name                                            Stmts   Miss  Cover
-------------------------------------------------------------------
app.py                                             14     14     0%
src/__init__.py                                     0      0   100%
src/apps/__init__.py                               12      0   100%
src/apps/account/__init__.py                        0      0   100%
src/apps/account/controller.py                     15      0   100%
src/apps/account/model.py                          13      0   100%
src/apps/account/repository.py                     44      6    86%
src/apps/account/schema.py                         10      0   100%
src/apps/account/service.py                        22      0   100%
src/apps/user/controller.py                        10      0   100%
src/apps/user/model.py                              4      0   100%
src/apps/user/repository.py                        10      2    80%
src/apps/user/service.py                           16      0   100%
src/libs/__init__.py                                2      0   100%
src/libs/api/error_code.py                         11      0   100%
src/libs/api/error_handler.py                      13      2    85%
src/libs/api/exception.py                          13      0   100%
src/libs/api/util.py                               35      0   100%
src/libs/api/validator.py                          23      0   100%
src/libs/cipher.py                                 17      0   100%
src/libs/db_manager.py                             23      2    91%
src/libs/token.py                                  10      0   100%
tests/apps/account/test_account_controller.py      53      0   100%
tests/apps/account/test_account_repository.py      45      0   100%
tests/apps/account/test_account_service.py         69      0   100%
tests/apps/user/test_user_controller.py            32      0   100%
tests/apps/user/test_user_repository.py            27      0   100%
tests/apps/user/test_user_service.py               24      0   100%
tests/libs/test_encrypt.py                         26      0   100%
tests/libs/test_error_code.py                       3      0   100%
tests/libs/test_util.py                            24      0   100%
-------------------------------------------------------------------
TOTAL                                             620     26    96%
```

<br>

![graph](https://codecov.io/gh/robert-min/ArtAPI-FastAPI/graphs/tree.svg?token=2MUZJH61VC)
