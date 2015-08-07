%define slurm_web_ver 1.1.2

Name:           slurm-web
Version:        %{slurm_web_ver}
Release:        1%{?dist}
Summary:        Slurm-web is web application that serves as web frontend to Slurm workload manager.

License:        GPLv2+
URL:            http://edf-hpc.github.io/slurm-web/
Source0:        https://github.com/edf-hpc/slurm-web/archive/debian/%{slurm_web_ver}.tar.gz

BuildArch:      noarch
Requires:       slurm-web-dashboard
Requires:       slurm-web-restapi

%description
Slurm-web is web application that serves as web frontend to Slurm workload manager.

%package dashboard
Summary:    Slurm-web interface
BuildArch:  noarch
Requires:   libjs-bootstrap
Requires:   js-jquery
Requires:   libjs-jquery-flot
Requires:   httpd
Requires:   httpd-devel

%description dashboard
The role of the dashboard is to show to users, administrators and decidors all supercomputer runtime data in a graphical and attractive way. It is a web GUI that aims to be user-friendly, beautiful and clean. The dashboard is developed in HTML and Javascript. It is designed to be used with any modern web browser with fairly decent support of HTML5, Javascript and CSS.

%package restapi
Summary:    Slurm-web backend api
BuildArch:  noarch
Requires:   python
Requires:   clustershell
#Requires:   python-clustershell
Requires:   python-flask
Requires:   python-pyslurm

%description restapi
The role of the API is to serve raw runtime data about a system (typically a supercomputer) running Slurm. All data are delivered in common and standard JSON format. This backend API is developed in Python programming language.

%prep
%setup -n slurm-web-debian-%{slurm_web_ver}

%build

%install

# Install apache conf files
install -d $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m644 conf/slurm-web-dashboard.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/slurm-web-dashboard.conf
install -m644 conf/slurm-web-restapi.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/slurm-web-restapi.conf

# Install racks configuration file
install -d $RPM_BUILD_ROOT/etc/slurm-web
install -m644 conf/racks.xml $RPM_BUILD_ROOT/etc/slurm-web/racks.xml

# Install remaining dashboard files
install -d $RPM_BUILD_ROOT/usr/share/slurm-web/dashboard/css
install -d $RPM_BUILD_ROOT/usr/share/slurm-web/dashboard/static
install -d $RPM_BUILD_ROOT/usr/share/slurm-web/dashboard/js
install -m644 html/index.html $RPM_BUILD_ROOT/usr/share/slurm-web/dashboard/index.html
install -m644 css/dashboard.css $RPM_BUILD_ROOT/usr/share/slurm-web/dashboard/css/dashboard.css
install -m644 static/logo.png $RPM_BUILD_ROOT/usr/share/slurm-web/dashboard/static/logo.png
install -m644 js/slurm-dashboard.js $RPM_BUILD_ROOT/usr/share/slurm-web/dashboard/js/slurm-dashboard.js

# Install remaining restapi files
install -d $RPM_BUILD_ROOT/usr/share/slurm-web/restapi/schema/dtd
install -m644 rest/slurmrestapi.py $RPM_BUILD_ROOT/usr/share/slurm-web/restapi/slurm-web-restapi.wsgi
install -m644 rest/slurmrestapi.py $RPM_BUILD_ROOT/usr/share/slurm-web/restapi/slurmrestapi.py
install -m644 schema/racks.dtd $RPM_BUILD_ROOT/usr/share/slurm-web/restapi/schema/dtd/racks.dtd

# Install doc files
install -m644 README.md $RPM_BUILD_ROOT/usr/share/slurm-web/README.md
install -m644 COPYING $RPM_BUILD_ROOT/usr/share/slurm-web/COPYING

%post
# start apache server if not already started, otherwise restart
systemctl restart httpd

#start flask app
#python $RPM_BUILD_ROOT/usr/share/slurm-web/restapi/slurmrestapi.py

%files
%doc /usr/share/slurm-web/README.md
%doc /usr/share/slurm-web/COPYING

%files dashboard
/etc/httpd/conf.d/slurm-web-dashboard.conf
/usr/share/slurm-web/dashboard/css/dashboard.css
/usr/share/slurm-web/dashboard/static/logo.png
/usr/share/slurm-web/dashboard/js/slurm-dashboard.js
/usr/share/slurm-web/dashboard/index.html

%files restapi
/etc/slurm-web/racks.xml
/etc/httpd/conf.d/slurm-web-restapi.conf
/usr/share/slurm-web/restapi/slurm-web-restapi.wsgi
/usr/share/slurm-web/restapi/slurmrestapi.py
/usr/share/slurm-web/restapi/slurmrestapi.pyc
/usr/share/slurm-web/restapi/slurmrestapi.pyo
/usr/share/slurm-web/restapi/schema/dtd/racks.dtd

%changelog
