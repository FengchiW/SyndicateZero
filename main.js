const electron = require('electron');
const url = require('url');
const path = require('path');

const { app, BrowserWindow, Menu } = electron;

let mainWindow;

app.on('ready', function() {

    mainWindow = new BrowserWindow({});

    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file',
        slashes: true
    }));

    const mainMenu = Menu.buildFromTemplate(menuTemplate)

    Menu.setApplicationMenu(mainMenu)
});

const menuTemplate = [{
    label: 'File',
    submenu: [{
            label: 'Add',
            click() {

            }
        },
        {
            label: 'Quit',
            accelerator: process.platform == 'darwin' ? 'Command+Q' : 'Ctrl+Q',
            click() {
                app.quit()
            }
        }
    ]
}]