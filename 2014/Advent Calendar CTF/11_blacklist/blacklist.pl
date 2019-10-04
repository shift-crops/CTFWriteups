use Mojolicious::Lite;
use DBI;

# enjoy~
my $BLACKLIST_CHAR = qr/['*=]/;
my $BLACKLIST_WORD = qr/select|insert|update|from|where|order|union|information_schema/;

my $dbh = DBI->connect('dbi:mysql:blacklist', 'blacklist', $ENV{BLACKLIST_PASSWORD});
helper dbh => sub { $dbh };

get '/' => sub {
    my $self = shift;
    my $ip = $self->tx->remote_address;
    my $agent = $self->req->headers->user_agent;
    # remove evil comments
    $agent =~ s!/\*.*\*/!!g;
    # disallow this one
    die 'no hack' if $agent =~ /\)\s*,\s*\(/;
    $self->dbh->do(
        "INSERT INTO access_log (accessed_at, agent, ip) VALUES (NOW(), '$agent', '$ip')"
    );
    my $access = $self->dbh->selectall_arrayref(
        "SELECT * FROM access_log WHERE ip = '$ip' ORDER BY accessed_at DESC LIMIT 10",
        {Slice => {}}
    );
    return $self->render('index', ip => $ip, access => $access);
};

get '/search' => sub {
    my $self = shift;
    my $ip = $self->param('ip');
    $ip =~ s/$BLACKLIST_CHAR//g;
    $ip =~ s/$BLACKLIST_WORD//g;
    my $id = $self->param('id');
    $id =~ s/$BLACKLIST_CHAR//g;
    $id =~ s/$BLACKLIST_WORD//g;
    my ($agent) = $self->dbh->selectrow_array(
        "SELECT agent FROM access_log WHERE ip = '$ip' AND id = '$id'",
        {Slice => {}}
    );
    if ($agent) {
        $agent =~ s/$BLACKLIST_CHAR//g;
        $agent =~ s/$BLACKLIST_WORD//g;
        my $access = $self->dbh->selectall_arrayref(
            "SELECT * FROM access_log WHERE ip = '$ip' AND agent LIKE '$agent' ORDER BY accessed_at DESC LIMIT 10",
            {Slice => {}}
        );
        return $self->render('search', agent => $agent, access => $access);
    } else {
        return $self->render_not_found;
    }
};

get '/source' => sub {
    my $self = shift;
    my $src = do {
        open my $fh, '<', __FILE__ or die $!;
        local $/; <$fh>;
    };
    return $self->render(text => $src, format => 'txt');
};

app->start;

__DATA__
@@ index.html.ep
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>blacklist</title>
</head>
<body>
    <p>sqli, sqli, sqli~~~ we have blacklist. see <a href="/source">source</a>.</p>
    <h2><%= stash 'ip' %>:</h3>
    <ul>
    % my $access = stash 'access';
    % for (@$access) {
        <li>[<%= $_->{accessed_at} %>] "<%= $_->{agent} %>" <a href="<%== url_for('/search')->query(ip => $_->{ip}, id => $_->{id}) %>">search</a></li>
    % }
    </ul>
</body>
</html>

@@ search.html.ep
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>blacklist</title>
</head>
<body>
    <h2>search with "<%= stash 'agent' %>"</h3>
    <ul>
    % for (@$access) {
        <li>[<%= $_->{accessed_at} %>] "<%= $_->{agent} %>"</li>
    % }
    </ul>
</body>
</html>

@@ not_found.html.ep
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>not found</title>
    <style>body{font-size:64px;}</style>
</head>
<body>
    <pre>             _      __                       _
 _ __   ___ | |_   / _| ___  _   _ _ __   __| |
| '_ \ / _ \| __| | |_ / _ \| | | | '_ \ / _` |
| | | | (_) | |_  |  _| (_) | |_| | | | | (_| |_ _ _
|_| |_|\___/ \__| |_|  \___/ \__,_|_| |_|\__,_(_|_|_)</pre>
</body>
</html>
