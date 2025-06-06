# Contributing

All contributions, whether in the form of bug reports, pull requests, and documentation updates are very welcome!

## Development task runner

We use [`just`](https://github.com/casey/just) to execute common tasks. It is available for any platform. Once installed, you can see a list of available commands by running `just --list`.

## Dependencies

We use `uv` to manage the Python [dependencies](https://docs.astral.sh/uv/).
If you don't have `uv`, you should install with `just uv-install`.

To install dependencies and prepare [`pre-commit`](https://pre-commit.com/) hooks you would need to run the `bootstrap` command:

```bash
just bootstrap
```

## Running updates

After pulling new updates from the repository you can quickly install updated dependencies and run database migrations by running `just bootstrap`.

## Codestyle

After installation you may execute code formatting.

```bash
just fmt
```

### Checks

Many checks are configured for this project.

To run your test suite:

```bash
just test
```

Or you can run testing for linting and multiple supported Python versions via:

```bash
just tox
```

To use pyright for type checking run:
```bash
just check-types
```

To run linting:

```bash
just lint
```

The `just safety` command will look at the security of your code.

### Before submitting

Before submitting your code please do the following steps:

1. Add any changes you want
2. Add tests for the new changes
3. Edit documentation if you have changed something significant
4. Run `just fmt` to format your changes.
5. Run `just check-all` to ensure that types, security and docstrings are okay.
6. Run `just tox` to ensure all tests pass.

## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.
