package_name="yt-dlp"

if pacman -Qi $package_name &> /dev/null; then
    echo "El paquete $package_name ya está instalado."
else
    echo "El paquete $package_name no está instalado. Iniciando la instalación..."
    sudo pacman -S --noconfirm $package_name
    echo "La instalación de $package_name ha finalizado."
fi