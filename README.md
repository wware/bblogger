BBLogger
========

This is a logging system for a bunch of machines running on a subnet. One machine,
the aggregator of logging information, runs an HTTP server so that Python processes
anywhere on the subnet can submit log messages by HTTP POSTs.

Configuration is done with a very simple YAML file on the server.

```yaml
---
foo: DEBUG
bar: INFO
```

The client code does normal Python logging using the names `foo` and `bar`.
If your logging call constructs arguments, be sure to use `isEnabledFor` to
avoid the effort of construction if the logger is not enabled for that level,
like this.

```python
    ...blah blah blah...
    if logger.isEnabledFor(logging.DEBUG):
        complex_arg = ...laborious computation...
        logger.debug(complex_arg)
    ...more blah blah blah...
```

The only configuration needed on the client side is to set the `HOST` variable in
`bblogger/__init__.py`, to point to the log aggregator machine.


You'll probably be running several machines as clients across a subnet, each
with its own copy of `/etc/bblogger.conf`. That still leaves you the freedom to change
bitmasks on the server's copy, as long as the channel names and bit
definitions don't change, and those are likely to be pretty stable over the
course of a development effort.

The logger has a couple of additional logging methods operating at the `DEBUG`
level. The `pprint` method performs a `pprint.pformat` of the argument, so that's
handy for complicated data types. The `stack` method shows the call stack at the
point of logging, with an optional text message.
