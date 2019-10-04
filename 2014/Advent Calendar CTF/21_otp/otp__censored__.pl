#!/usr/bin/env perl
use Mojolicious::Lite;
use DBI;

my $dbh = DBI->connect(
    'dbi:SQLite:dbname=./otp.db', '', '',
    +{
        RaiseError     => 1,
        sqlite_unicode => 1,
    }
);
app->helper(dbh => sub { $dbh });

get '/' => sub {
    my $c = shift;
    my ($token, $pass) = gen_otp();
    my $expire = time() + 10;
    $c->dbh->do('INSERT INTO otp VALUES (?, ?, ?)', undef, $token, $pass, $expire);
    $c->render('index', token => $token);
};

post '/' => sub {
    my $c = shift;
    my $token = $c->req->param('token');
    # tiny firewall, but powerful :P
    if ($token =~ /sqlite/i) {
        $c->render('error', message => "no hack.");
        return;
    }
    my $time = time();
    my ($expire) = $c->dbh->selectrow_array(
        "SELECT ###CENSORED### FROM otp WHERE ###CENSORED### = '$token' AND ###CENSORED### < $time",
    );
    if ($expire) {
        $c->render('error', message => "otp expired at $expire");
    } else {
        my $pass = $c->req->param('pass');
        my ($ok) = $c->dbh->selectrow_array(
            'SELECT 1 FROM otp WHERE ###CENSORED### = ? AND ###CENSORED### = ?', undef, $token, $pass,
        );
        $c->render('auth', ok => $ok);
    }
    $c->dbh->do(
        'DELETE FROM otp WHERE ###CENSORED### = ?', undef, $token
    );
};

sub gen_otp {
    open my $fh, '<:raw', '/dev/urandom' or die $!;
    read $fh, my $token, 8;
    $token = unpack 'H*', $token;
    read $fh, my $pass, 16;
    $pass = unpack 'H*', $pass;
    return ($token, $pass);
}

app->start;
__DATA__

@@ index.html.ep
% layout 'default';
% title 'OTP';

<form method="POST">
  <input type="hidden" name="token" value="<%= $token %>" />
  <input type="text" name="pass" />
  <input type="submit" value="auth" />
</form>

@@ auth.html.ep
% layout 'default';
% title 'Authentication | OTP';

% if ($ok) {
<p>authentication succeeded.<br />the flag is: ###CENSORED###</p>
% } else {
<p>authentication failed.</p>
% }

@@ error.html.ep
% layout 'default';
% title 'Error | OTP';

<p><%= $message %></p>

@@ layouts/default.html.ep
<!DOCTYPE html>
<html>
  <head>
    <title><%= title %></title>
  </head>
  <style>
body, input {
  color: #fff;
  background: #333;
  font-family: monospace;
  font-size: 150%;
}
.container {
  width: 100%;
  margin-top: 50px;
  text-align: center;
}
  </style>
  <body>
<div class="container">
<%= content %>
</div>
  </body>
</html>
