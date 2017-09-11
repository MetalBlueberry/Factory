from Factory.Building import Building

def find_building_in_engine(engine):
    childrens = engine.rootObjects()[0].children()
    building = None
    for children in childrens:
        if type(children) is Building:
            building = children
            break
    if building is None:
        raise Exception("Building missing, add it to the window in qml")

    return building