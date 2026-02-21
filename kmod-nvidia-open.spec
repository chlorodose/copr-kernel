Name:           kmod-nvidia-open 
Version:        NV_VERSION 
Release:        1 
Summary:        Compatibilityi dummy package for nvidia kmod 
License:        None 
BuildArch:      noarch

Provides:       %{name} = 3:%{version}
Provides:       nvidia-kmod = 3:%{version} 

Requires:       modalias(of:N*T*Cnvidia_tegra2[36]4-display) = %{version}

%description
This is a dummy package.

%files
