//This function is for adjust the width of the mind map based on it's type and also based on screen width
function adjustResponsiveZoom(diagram, viewType) {
  const screenWidth = window.innerWidth;
  const nodeCount = diagram.nodes.count;
    // Define scaling factors based on screen width
    const scalingFactor = screenWidth > 1200 ? 1 : screenWidth > 800 ? 0.7 : 0.4;

    // Define zoom levels based on view type and node count
    const zoomLevels = {
      "first": nodeCount > 10 ? 0.5 : 0.9,
      "second": nodeCount > 12 ? 0.2 : 0.7,
      "third": nodeCount > 12 ? 0.4 : 0.8
    };
  
    // Adjust the zoom level
    diagram.scale = (zoomLevels[viewType] || 1.0) * scalingFactor;
    diagram.zoomToFit();
  
  
  }

// Function to initialize the first view
function initializeFirstView(gojs_model) {
  
  
  const mindMapDiagram = new go.Diagram("mind", {
    "undoManager.isEnabled": true,
    layout: new go.TreeLayout({ angle: 90, layerSpacing: 35 }),
  });
    // Adjust the zoom level after the diagram has been laid out
     mindMapDiagram.addDiagramListener("InitialLayoutCompleted", function() {

      adjustResponsiveZoom(mindMapDiagram, 'first');
      mindMapDiagram.alignDocument(go.Spot.Center, go.Spot.Center);
    });
    // Add responsiveness for window resizing
    window.addEventListener('resize', function () {
      adjustResponsiveZoom(mindMapDiagram, 'first');
      mindMapDiagram.alignDocument(go.Spot.Center, go.Spot.Center); 
    });

  mindMapDiagram.nodeTemplate = new go.Node("Spot", {
    background: "transparent",
    click: (e, obj) => {
      const nodeData = obj.part.data;
      generate_subtopic_window(nodeData.name, obj);
    }
  })
    .add(
      new go.Shape("Circle", {
        width: 80, height: 80,
        fill: "white", strokeWidth: 2, stroke: "black"
      })
        .bind("fill", "color"),
      new go.TextBlock("Default Text", {
        font: "bold 10px sans-serif",
        stroke: "black",
        textAlign: "center",
        verticalAlignment: go.Spot.Center,
        margin: 0,
        wrap: go.TextBlock.WrapFit,
        width: 70
      })
        .bind("text", "name")
    );

    
  mindMapDiagram.model = new go.TreeModel(gojs_model);


}

// Function to initialize the second view
function initializeSecondView(gojs_model) {
  
  const init = () => {
    const myDiagram = new go.Diagram('mind', {
      'commandHandler.copiesTree': true,
      'commandHandler.copiesParentKey': true,
      'commandHandler.deletesTree': true,
      'draggingTool.dragsTree': true,
      'undoManager.isEnabled': true,
      'draggingTool.isEnabled': false, // Disable dragging of nodes
    });
  
   
       // Adjust the zoom level after the diagram has been laid out
       myDiagram.addDiagramListener("InitialLayoutCompleted", function() {
        adjustResponsiveZoom(myDiagram, 'second');
        myDiagram.alignDocument(go.Spot.Center, go.Spot.Center); 
      });
      // Add responsiveness
      window.addEventListener('resize', function() {
        adjustResponsiveZoom(myDiagram, 'second');
        myDiagram.alignDocument(go.Spot.Center, go.Spot.Center); 
      });
  
    myDiagram.addDiagramListener('Modified', (e) => {
      const button = document.getElementById('SaveButton');
      if (button) button.disabled = !myDiagram.isModified;
      const idx = document.title.indexOf('*');
      if (myDiagram.isModified) {
        if (idx < 0) document.title += '*';
      } else {
        if (idx >= 0) document.title = document.title.slice(0, idx);
      }
    });

    myDiagram.nodeTemplate = new go.Node('Vertical', {
      selectionObjectName: 'TEXT',
      click: (e, obj) => {
        const nodeData = obj.part.data;
        generate_subtopic_window(nodeData.name, obj); // Adjusted key from "name" to "text"
        movable: false // Disable manual movement of nodes
      }
    })
      .bindTwoWay('location', 'loc', go.Point.parse, go.Point.stringify)
      .bind('locationSpot', 'dir', (d) => spotConverter(d, false))
      .add(
        new go.TextBlock({
          name: 'TEXT',
          minSize: new go.Size(30, 15),
          editable: false
          
        })
          .bindTwoWay('text', 'name')
          .bindTwoWay('scale')
          .bindTwoWay('font'),
        new go.Shape('LineH', {
          stretch: go.Stretch.Horizontal,
          strokeWidth: 3,
          height: 3,
          portId: '',
          fromSpot: go.Spot.LeftRightSides,
          toSpot: go.Spot.LeftRightSides
        })
          .bind('stroke', 'brush')
          .bind('fromSpot', 'dir', (d) => spotConverter(d, true))
          .bind('toSpot', 'dir', (d) => spotConverter(d, false))
      );

    myDiagram.nodeTemplate.selectionAdornmentTemplate = new go.Adornment('Spot')
      .add(
        new go.Panel('Auto')
          .add(
            new go.Shape({
              fill: null,
              stroke: 'dodgerblue',
              strokeWidth: 3
            }),
            new go.Placeholder({ margin: new go.Margin(4, 4, 0, 4) })
          ),
       
      );

    myDiagram.nodeTemplate.contextMenu = go.GraphObject.build('ContextMenu')
      .add(
        go.GraphObject.build('ContextMenuButton')
          .add(new go.TextBlock('Bigger', { click: (e, obj) => changeTextSize(obj, 1.1) })),
        go.GraphObject.build('ContextMenuButton')
          .add(new go.TextBlock('Smaller', { click: (e, obj) => changeTextSize(obj, 1 / 1.1) })),
        go.GraphObject.build('ContextMenuButton')
          .add(new go.TextBlock('Bold/Normal', { click: (e, obj) => toggleTextWeight(obj) })),
        go.GraphObject.build('ContextMenuButton')
          .add(new go.TextBlock('Copy', { click: (e, obj) => e.diagram.commandHandler.copySelection() })),
        go.GraphObject.build('ContextMenuButton')
          .add(new go.TextBlock('Delete', { click: (e, obj) => e.diagram.commandHandler.deleteSelection() })),
        go.GraphObject.build('ContextMenuButton')
          .add(new go.TextBlock('Undo', { click: (e, obj) => e.diagram.commandHandler.undo() })),
        go.GraphObject.build('ContextMenuButton')
          .add(new go.TextBlock('Redo', { click: (e, obj) => e.diagram.commandHandler.redo() })),
        go.GraphObject.build('ContextMenuButton')
          .add(new go.TextBlock('Layout', {
            click: (e, obj) => {
              const adorn = obj.part;
              adorn.diagram.startTransaction('Subtree Layout');
              layoutTree(adorn.adornedPart);
              adorn.diagram.commitTransaction('Subtree Layout');
            }
          }))
      );

    myDiagram.linkTemplate = new go.Link({
      curve: go.Curve.Bezier,
      fromShortLength: -2,
      toShortLength: -2,
      selectable: false
    })
      .add(
        new go.Shape({ strokeWidth: 3 })
          .bindObject('stroke', 'toNode', (n) => n.data.brush || 'black')
      );

    myDiagram.contextMenu = go.GraphObject.build('ContextMenu')
      .add(
        go.GraphObject.build('ContextMenuButton', {
          click: (e, obj) => e.diagram.commandHandler.pasteSelection(e.diagram.toolManager.contextMenuTool.mouseDownPoint)
        })
          .bindObject('visible', '',
            (o) => o.diagram && o.diagram.commandHandler.canPasteSelection(o.diagram.toolManager.contextMenuTool.mouseDownPoint))
          .add(new go.TextBlock('Paste')),
        go.GraphObject.build('ContextMenuButton', {
          click: (e, obj) => e.diagram.commandHandler.undo()
        })
          .bindObject('visible', '', (o) => o.diagram && o.diagram.commandHandler.canUndo())
          .add(new go.TextBlock('Undo')),
        go.GraphObject.build('ContextMenuButton', {
          click: (e, obj) => e.diagram.commandHandler.redo()
        })
          .bindObject('visible', '', (o) => o.diagram && o.diagram.commandHandler.canRedo())
          .add(new go.TextBlock('Redo')),
        go.GraphObject.build('ContextMenuButton')
          .add(new go.TextBlock('Save', { click: () => save() })),
        go.GraphObject.build('ContextMenuButton')
          .add(new go.TextBlock('Load', { click: () => load() }))
      );

    myDiagram.addDiagramListener('SelectionMoved', (e) => {
      const rootX = myDiagram.findNodeForKey(0).location.x;
      myDiagram.selection.each((node) => {
        if (node.data.parent !== 0) return;
        const nodeX = node.location.x;
        if (rootX < nodeX && node.data.dir !== 'right') {
          updateNodeDirection(node, 'right');
        } else if (rootX > nodeX && node.data.dir !== 'left') {
          updateNodeDirection(node, 'left');
        }
        layoutTree(node);
      });
    });
   
    myDiagram.model = new go.TreeModel(gojs_model);
   
  };

  const spotConverter = (dir, from) => {
    if (dir === 'left') {
      return from ? go.Spot.Left : go.Spot.Right;
    } else {
      return from ? go.Spot.Right : go.Spot.Left;
    }
  };

  const changeTextSize = (obj, factor) => {
    const adorn = obj.part;
    adorn.diagram.startTransaction('Change Text Size');
    const node = adorn.adornedPart;
    const tb = node.findObject('TEXT');
    tb.scale *= factor;
    adorn.diagram.commitTransaction('Change Text Size');
  };

  const toggleTextWeight = (obj) => {
    const adorn = obj.part;
    adorn.diagram.startTransaction('Change Text Weight');
    const node = adorn.adornedPart;
    const tb = node.findObject('TEXT');
    const idx = tb.font.indexOf('bold');
    if (idx < 0) {
      tb.font = 'bold ' + tb.font;
    } else {
      tb.font = tb.font.slice(idx + 5);
    }
    adorn.diagram.commitTransaction('Change Text Weight');
  };

  const updateNodeDirection = (node, dir) => {
    myDiagram.model.setDataProperty(node.data, 'dir', dir);
  };

  const layoutTree = (node) => {
    const treeLayout = new go.TreeLayout();
    treeLayout.angle = 90;
    treeLayout.layerSpacing = 35;
    treeLayout.isOngoing = false;
    myDiagram.layout = treeLayout;
    myDiagram.layoutDiagram();
  };



  const save = () => {
     // Show the diagram's model in JSON format
 
    document.getElementById('mySavedModel').value = myDiagram.model.toJson();
    myDiagram.isModified = false;
  }

 
  const load = () => {
    myDiagram.model = go.Model.fromJson(document.getElementById('mySavedModel').value);
    // if any nodes don't have locations assigned from the model, force a layout of everything
    if (myDiagram.nodes.any(n => !n.location.isReal())) layoutAll();
  }
    

  init();
}

 // Function to initialize the third view
function initializeThirdView(gojs_model) {
 
  function init() {
    const thirdObject = go.GraphObject.make;  // for conciseness in defining templates
    const nodeDataArray = gojs_model;

    // Create the Diagram
    const diagram = thirdObject(go.Diagram, "mind", {
      layout: thirdObject(go.TreeLayout, { angle: 90, layerSpacing: 35 })
    });

      // Adjust the zoom level after the diagram has been laid out
      diagram.addDiagramListener("InitialLayoutCompleted", function() {
        adjustResponsiveZoom(diagram, 'third');
        diagram.alignDocument(go.Spot.Center, go.Spot.Center);
      });
          // Add responsiveness
      window.addEventListener('resize', function() {
        adjustResponsiveZoom(diagram, 'third');
        diagram.alignDocument(go.Spot.Center, go.Spot.Center);
      });

    // Define the Node template
    diagram.nodeTemplate = thirdObject(
      go.Node, "Auto",
      {
        click: (e, obj) => {
          const nodeData = obj.part.data;
          generate_subtopic_window(nodeData.name, obj);
          console.log(nodeData);
        }
      },
      thirdObject(go.Shape, "RoundedRectangle", { strokeWidth: 0 },
        new go.Binding("fill", "color")),
      thirdObject(go.TextBlock, { margin: 8, font: "bold 12px sans-serif" },
        new go.Binding("text", "name"))
    );

    // Define the Link template
    diagram.linkTemplate = thirdObject(go.Link,
      thirdObject(go.Shape)
    );

    // Create the model using the node data array
    diagram.model = new go.TreeModel(nodeDataArray);
      


    // Function to get a random color
    function getRandomColor() {
      const colors = ["#f1916d", "#473e66", "#bd83b8", "#f5d7db"];
      return colors[Math.floor(Math.random() * colors.length)];
    }
  }

  init();
}

// Function to clear the diagram
function clearDiagram(divId) {
  const diagram = go.Diagram.fromDiv(divId);
  if (diagram) {
    diagram.div = null;
  }
}

// Function to format the data for the first view
function firstViewFormat(data) {
  const gojs_model = [];
  const title = data["mainTitle"];
  const title_key = "1";
  gojs_model.push({ "key": title_key, "name": title });

  const colors = ["#f1916d", "#473e66", "#bd83b8", "#f5d7db"];
  data["subtitles"].forEach((subtitle, idx) => {
    const subtitle_key = (idx + 2).toString();
    gojs_model.push({
      "key": subtitle_key,
      "parent": title_key,
      "name": subtitle["subtitle"],
      "color": colors[idx % colors.length],
      "paragraph": subtitle["paragraphs"].join(""),
    });
  });
 
  return gojs_model;
}

// Function to apply the first view
function applyFirstView() {
  clearDiagram("mind");
  const gojs_model = firstViewFormat(output);
  initializeFirstView(gojs_model);
}

// Function to format the data for the second view
function secondViewFormat(data) {
    const gojs_model = [];
    const main_title = data["mainTitle"];
    const subtitles = data["subtitles"];
    // Predefined list of colors
    const colors = ["skyblue", "darkseagreen", "palevioletred", "coral", "gold", "lightgreen", "lightsalmon"];

    // Add the main title as the central node
    gojs_model.push({ "key": 0, "name": main_title, "loc": "0 0", "brush": "white" });

    // Dynamic radius and horizontal offset based on the number of subtitles
    const subtitle_count = subtitles.length;
    const base_radius = 200; // Minimum radius
    const base_horizontal_offset = 150; // Minimum horizontal offset

    // Radius increases logarithmically based on the number of subtitles
    const radius = base_radius + (50 * Math.log2(subtitle_count + 1));
    // Horizontal offset increases to prevent overlapping for large number of nodes
    const horizontal_offset = base_horizontal_offset + (20 * Math.log2(subtitle_count + 1));

    // Calculate the angle step for spacing between nodes
    const angle_step = 360 / subtitle_count;

    let key = 1;
    for (let index = 0; index < subtitle_count; index++) {
        const angle = (index * angle_step) * (Math.PI / 180);
        const x = (radius + horizontal_offset) * Math.cos(angle);
        const y = radius * Math.sin(angle);
        const color = colors[index % colors.length];
        
        gojs_model.push({
            "key": key,
            "parent": 0,
            "name": subtitles[index]["subtitle"],
            "brush": color,
            "loc": `${x} ${y}`,
            "paragraph": subtitles[index]["paragraphs"].join("")
        });
        key += 1;
    }
    return gojs_model;
}

  


// Function to apply the second view
function applySecondView() {
  clearDiagram("mind");
  const gojs_model = secondViewFormat(output);
  initializeSecondView(gojs_model);
}

// Function to format the data for the third view
function thirdViewFormat(data) {
  const gojs_model = [];
  const main_title = data["mainTitle"];
  const subtitles = data["subtitles"];
  // Predefined list of colors
  const colors = ["skyblue", "darkseagreen", "palevioletred", "coral", "gold", "lightgreen", "lightsalmon"];
  gojs_model.push({ "key": 1, "name": main_title, "color": "lightblue" });
  let key = 2;
  subtitles.forEach((subtitle) => {
    const color = colors[Math.floor(Math.random() * colors.length)];
    gojs_model.push({
      "key": key,
      "parent": 1,
      "name": subtitle["subtitle"],
      "color": color,
      "paragraph": subtitle["paragraphs"].join("")
    });
    key += 1;
  });
  return gojs_model;
}

// Function to apply the third view
function applyThirdView() {
  clearDiagram("mind");
  const gojs_model = thirdViewFormat(output);
  initializeThirdView(gojs_model);
  adjustResponsiveZoom(diagram, "third");
}

// Add event listeners to the buttons
  window.onload=function(){
    document.getElementById('first-view').addEventListener('click', () => {
        applyFirstView();
    });
  
    document.getElementById('second-view').addEventListener('click', () => {
        applySecondView();
    });
  
    document.getElementById('third-view').addEventListener('click', () => {
        applyThirdView();
    });
  
  }
