from ipaddress import ip_address
from ipaddress import ip_network


class InvalidIPRangeSpecification(ValueError):
    """Error in specification of allowed IP range.
    """


def parse_ip_range(ip_range):
    """Parse an IP range specification and return a list of allowed networks.

    IP ranges may be specified as a single IP address or as a network in CIDR
    notation using the slash-suffix.

    Multiple ranges may be provided in comma-separated form.

    Examples:

    192.168.1.1
    192.168.0.0/16
    192.168.1.1, 10.0.0.0/8
    """
    ranges = [rng.strip() for rng in to_unicode(ip_range).split(u',')]
    networks = []
    for rng in ranges:
        try:
            network = ip_network(rng)
        except ValueError as exc:
            raise InvalidIPRangeSpecification(exc.message)
        networks.append(network)
    return networks


def permitted_ip(client_ip, ip_range):
    """Return True if a client IP is in the given range(s), False otherwise.
    """
    try:
        allowed_networks = parse_ip_range(ip_range)
    except InvalidIPRangeSpecification:
        return False

    ip = ip_address(to_unicode(client_ip))
    return any(ip in net for net in allowed_networks)


def to_unicode(ip_spec):
    """Ensure ip_spec is unicode, decoding it if necessary.

    The `ipaddress` module (as opposed to `py2-ipaddress`) absolutely
    requires IP specifications to be passed in as unicode. We therefore make
    sure the ip_spec is unicode, decoding it as ASCII if necessary (IP specs
    should never contain any non-ASCII characters).
    """
    if not isinstance(ip_spec, unicode):
        ip_spec = ip_spec.decode('ascii')
    return ip_spec
