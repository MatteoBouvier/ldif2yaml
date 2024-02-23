# ldifparse
Parse LDIF data into common text formats. It currently supports conversion to JSON and to YAML.

This is a thin wrapper around the [python-ldap](https://www.python-ldap.org/en/python-ldap-3.4.3/) package.

From:
```sh
$ ldapsearch -Q -L -Y EXTERNAL -H ldapi:/// -b dc=company,dc=com
version: 1

#
# LDAPv3
# base <dc=company,dc=com> with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#

# company.com
dn: dc=company,dc=com
objectClass: top
objectClass: dcObject
objectClass: organization
o: company
dc: company

# admin, company.com
dn: cn=admin,dc=company,dc=com
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP administrator

# search result

# numResponses: 3
# numEntries: 2
```

To :
```sh
$ ldapsearch -Q -L -Y EXTERNAL -H ldapi:/// -b dc=company,dc=com | ldifparse
cn=admin,dc=company,dc=com:
  cn: admin
  description: LDAP administrator
  objectClass:
  - simpleSecurityObject
  - organizationalRole
dc=company,dc=com:
  dc: company
  o: company
  objectClass:
  - top
  - dcObject
  - organization
```

## Installation

### with pip/pipx

The recommended way of installing **ldifparse** is through the pipx installer : 

```sh
pipx install ldifparse
```

**ldifparse** will be installed in an isolated environment but will be available globally as a shell application.

Alternatively, you can install **ldifparse** in an environment of your choosing with pip :

```sh
pip install ldifparse
```

### manually

You can also download the source code from github :

```sh
git clone https://github.com/MatteoBouvier/ldifparse.git
```

## Tips

We recommend also installing [jq](https://jqlang.github.io/jq/) for viewing and manipulating JSON in the terminal.
The YAML equivalent is [yq](https://github.com/mikefarah/yq).

## Usage

The simplest way to use **ldifparse** is by piping it some LDIF data : 

```sh
cat input.ldif | ldifparse
```

This will print a YAML version of the data to stdout.

### Output format

You can specify the ouput format with the `--output` parameter (`-o` for the short version). The output can either be
`json` or `yaml` (`-oj` and `-oy` are also accepted as shorthands).

### Tree structure

Instead of a perfect translation of LDIF to JSON/YAML, you can get a tree representation with the `--tree` (`-t`) 
parameter.


