https://github.com/docker/docker-credential-helpers

  

Para usar configurar o pass no Ubuntu:

```Bash
download "docker-credential-pass".
wget https://github.com/docker/docker-credential-helpers/releases/download/v0.6.0/docker-credential-pass-v0.6.0-amd64.tar.gz

unpack tar -xf docker-credential-pass-v0.6.0-amd64.tar.gz

# i couldn`t configure $PATH environment variable, so i copied unpacked file to /usr/bin directory.

# check that docker-credential-pass work. To do this, run command docker-credential-pass. You should see: "Usage: docker-credential-pass <store|get|erase|list|version>".

# install gpg and pass. 
apt-get install gpg pass


# Enter your name, mail, etc. You will get gpg-id like "5BB54DF1XXXXXXXXF87XXXXXXXXXXXXXX945A". Copy it to clipboard.
gpg --generate-key. 


pass init (paste from clipboard)

pass insert docker-credential-helpers/docker-pass-initialized-check and set the next password "pass is initialized" (without quotes).

pass show docker-credential-helpers/docker-pass-initialized-check. You should see pass is initialized.

docker-credential-pass list. You should see {} or another data. You shouldn`t see error like "pass store is uninitialized".

nano ~/.docker/config.json. Set in root node the next line "credsStore": "pass" save ctrl+o.

after docker login and etc.
```

GOG key root

  

Name: josenaldo

Email: josenaldo@gmail.com

Pass: 123mudar

  

```Bash
gpg: key A0A8C0E1119340B4 marked as ultimately trusted

gpg: directory '/root/.gnupg/openpgp-revocs.d' created

gpg: revocation certificate stored as '/root/.gnupg/openpgp-revocs.d/386718B9C19A735C9D31049FA0A8C0E1119340B4.rev'

public and secret key created and signed.

pub   rsa3072 2024-03-17 [SC] [expires: 2026-03-17]
386718B9C19A735C9D31049FA0A8C0E1119340B4
uid                      josenaldo josenaldo@gmail.com
sub   rsa3072 2024-03-17 [E] [expires: 2026-03-17]
```

  

  

```Bash
gpg: key A1E42ACEDFB48AE6 marked as ultimately trusted
gpg: revocation certificate stored as '/home/josenaldo/.gnupg/openpgp-revocs.d/43D132D7B8870B6F27E9AF57A1E42ACEDFB48AE6.rev'
public and secret key created and signed.

pub   rsa3072 2024-03-17 [SC] [expires: 2026-03-17]
      43D132D7B8870B6F27E9AF57A1E42ACEDFB48AE6
uid                      josenaldo <josenaldo@gmail.com>
sub   rsa3072 2024-03-17 [E] [expires: 2026-03-17]
```

Fonte:

[https://github.com/docker/docker-credential-helpers/issues/102](https://github.com/docker/docker-credential-helpers/issues/102)

[https://github.com/docker/docker-credential-helpers](https://github.com/docker/docker-credential-helpers)