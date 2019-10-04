#!/usr/bin/env perl
use Mojolicious::Lite;

app->secrets([$ENV{LOGINPAGE_SECRET}]);

get '/' => sub {
    my $self = shift;
    return $self->render('index',
        user => $self->session->{user},
        flag => $ENV{FLAG},
    );
};

get '/user' => sub {
    my $self = shift;
    my @users;
    if (open my $fh, '<', "user.txt") {
        while (defined(my $user = <$fh>)) {
            my ($name, $password, $is_admin) = split /:/, $user;
            unshift @users, ($is_admin == 1 ? "$name (admin)" : $name);
        }
    }
    return $self->render('user',
        users => \@users,
    );
};

get '/register' => 'register';

post '/register' => sub {
    my $self = shift;

    my $name = $self->param('name') // '';
    my $pass = $self->param('pass') // '';

    $name =~ s/[^\x21-\x7e]//g; # ascii only!
    $pass =~ s/[^\x21-\x7e]//g;

    open my $fh, '>>', 'user.txt' or die $!;
    print {$fh} "$name:$pass:0\n"; # you are not admin
    close $fh;

    $self->session->{user} = {
        name         => $name,
        pass         => $pass,
        give_me_flag => 0,
        admin        => 0,
    };

    return $self->redirect_to('/');
};

get '/login' => 'login';

post '/login' => sub {
    my $self = shift;

    my $name = $self->param('name') // '';
    my $pass = $self->param('pass') // '';

    my $ok = 0;
    my $is_admin;
    open my $fh, '<', "user.txt" or die $!;
    while (defined(my $user = <$fh>)) {
        chomp $user;
        my ($n, $p, $a) = split /:/, $user;
        if ($n eq $name && $p eq $pass) {
            $is_admin = $a;
            $ok = 1;
            last;
        }
    }

    if ($ok) {
        $self->session->{user} = {
            name         => $self->param('name'),
            pass         => $self->param('pass'),
            give_me_flag => 0,
            admin        => $is_admin,
        };
        return $self->redirect_to('/');
    } else {
        return $self->render(text => 'login failed...');
    }
};

app->start;
__DATA__

@@ index.html.ep
% layout 'default';
% title 'hello';

<p>loginpage</p>

% if ($user) {
<p>hello, <b><%= $user->{name} %></b> (password is: <%= $user->{pass} %>)</p>
    % if ($user->{admin}) {
<p>you are admin!</p>
        % if ($user->{give_me_flag}) {
<p>the flag is: <%= $flag %></p>
        % } else {
<p>cheer up :)</p>
        % }
    % }
% }

@@ user.html.ep
% layout 'default';
% title 'user list';

<ul>
% for my $user (@$users) {
    <li><%= $user %></li>
% }
</ul>

@@ register.html.ep
% layout 'default';
% title 'register';

<h2>register</h2>

<form method="post" action="/register">
    name: <input type="text" name="name" /><br />
    pass: <input type="text" name="pass" /><br />
    <input type="submit" value="register" />
</form>

@@ login.html.ep
% layout 'default';
% title 'login';

<h2>login</h2>

<form method="post" action="/login">
    name: <input type="text" name="name" /><br />
    pass: <input type="text" name="pass" /><br />
    <input type="submit" value="login" />
</form>

@@ layouts/default.html.ep
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title><%= title %> - loginpage</title>
</head>
<body>
    <p><a href="/">index</a> | <a href="/register">register</a> | <a href="/login">login</a> | <a href="/user">user list</a></p>
    <%= content %>
</body>
</html>
