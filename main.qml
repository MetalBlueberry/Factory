import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.3
import Factory 1.0


ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")
    id: base

    Building{
        id:building

    }
    Column{
        anchors.centerIn: parent
        Button{

            text: "check"
            onClicked:{
                console.log("Clicked")
                var x = 0
                for( x= 0; x < base.contentItem.children.length; x++){
                    console.log(base.contentItem.children[x])
                }
            }
        }
        Text {
            id: name
            text: building.storagesList.length
        }
        Row{
            spacing: 5
            Repeater{
                model: building.storagesList.length
                Text{
                    text: building.storagesList[index].idName + " : " + building.storagesList[index].itemCount
                }
            }
        }
        Row{
            spacing: 5
            Repeater{
                model: building.workersList.length
                Text{
                    text: building.workersList[index].idName + " : " + building.workersList[index].progress
                }
            }
        }

    }
    Component.onCompleted: {
        var x = 0
        console.log("contents")
        console.log(base.contentItem)
        for( x= 0; x < base.contentItem.children.length; x++){
            console.log(base.contentItem.children[x])
        }
    }

}
