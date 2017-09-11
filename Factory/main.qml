import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.3
import Factory 1.0

import QtQuick.Dialogs 1.2

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")
    id: base

    Building{
        id:building
        onDefaultInputChanged: {

            console.log(building.defaultInput)
            console.log(building.defaultInput.items)
        }
    }
    Column{
        spacing: 5
        Repeater{
            model: building.defaultInput.items.length
            Text{
                text: building.defaultInput.items[index].description
            }
        }

    }
    Column{
        anchors.centerIn: parent
        spacing: 10
        Button{

            text: "check"
            onClicked:{
                loadFileDialog.open()
            }
            FileDialog{
                id: loadFileDialog
                title: "Please choose input files"
                folder: shortcuts.home
                selectExisting: true
                selectMultiple: false
                selectFolder: true

                onAccepted: {
                    console.log("You chose: " + loadFileDialog.folder)

                }
                onRejected: {
                    console.log("Canceled")

                }
            }
        }

        Column{
            spacing: 5
            Repeater{
                model: building.storagesList.length
                Text{
                    text: building.storagesList[index].idName + " : " + building.storagesList[index].itemCount
                }
            }
        }
        Column{
            spacing: 5
            Repeater{
                model: building.workersList.length
                Text{
                    text: building.workersList[index].idName + " : " + building.workersList[index].progress + " - " +building.workersList[index].progressMessage
                }
            }
        }

    }

}
