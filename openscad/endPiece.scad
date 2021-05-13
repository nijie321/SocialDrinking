

pumpHolderWidth=50.25;
pumpHolderHeight=38.17;
pumpHolderThickness=10.15;


semiCircleDiameter=22; //16.36;
semiCircleRadius=semiCircleDiameter/2;

semiCircleHeight=26.54;
semiCircleThickness=7.23;


//difference(){
//    cube([pumpHolderWidth,pumpHolderThickness,pumpHolderHeight],center=true);
//
//    translate([0,(pumpHolderThickness/2)-(semiCircleThickness/2)+.001,(pumpHolderHeight/2) - (semiCircleHeight/2)]) color("red") union(){
//    rotate([90,0,0]) cylinder(h=pumpHolderThickness+5,r=semiCircleRadius, center=true);
//
//    color("red") translate([0,0,(semiCircleHeight/2)/2]) cube([semiCircleDiameter,pumpHolderThickness+5,semiCircleHeight/2],center=true);
//    }
//}

recHeight=32.96;
recWidth=33.45;
recThickness=6.3;

sideScrewDiameter=3.5;
sideScrewRadius=sideScrewDiameter/2;
sideScrewDepth=4.65;



cubeShape=6.38;


topPlateHeight= 23.44;//1.45;
topPlateOffset = 1.45;

module sideScrew(){
    cylinder(h=sideScrewDepth,r=sideScrewRadius,center=true);
}

module makeFourSideScrews(){
union(){
color("red") translate([(recWidth/2)-(sideScrewDepth/2),0,(recHeight/2) - (cubeShape/2)]) rotate([0,090,0]) sideScrew();
color("red") translate([-((recWidth/2)-(sideScrewDepth/2)),0,(recHeight/2) - (cubeShape/2)]) rotate([0,090,0]) sideScrew();

color("red") translate([((recWidth/2)-(sideScrewDepth/2)),0,-((recHeight/2) - (cubeShape/2))]) rotate([0,090,0]) sideScrew();
color("red") translate([-((recWidth/2)-(sideScrewDepth/2)),0,-((recHeight/2) - (cubeShape/2))]) rotate([0,090,0]) sideScrew();   
}

}




module endPieceBlock(){
difference(){
cube([recWidth,recThickness,recHeight],center=true);
makeFourSideScrews();
}
}


hookWidth=12;//7.40;
hookHeight=7;
hookThickness=5;

stopperWidth=(1/2)*hookWidth;
stopperHeight=(1/2)*hookHeight;


module recStopper(){
//difference(){
//    //hookHeight+2
//cube([hookWidth,recThickness,hookHeight+2],center=true);
//
//translate([(stopperWidth/2) + (hookWidth/2)-(stopperWidth),0,-stopperHeight/2]) union(){
//cube([stopperWidth,recThickness,stopperHeight],center=true);
//color("blue") translate([-((1/2)*stopperWidth)/2,0,2*((stopperHeight-1)/2)]) cube([(1/2)*stopperWidth,hookThickness,stopperHeight-1],center=true);
//}
//}

difference(){
cube([hookWidth,recThickness,hookHeight+2],center=true);
    translate([1.5,0,-(hookHeight/1.5)/2]) cube([hookWidth/4,recThickness,hookHeight/1.2],center=true);
}
}




module circleStopper(){
difference(){
rotate([90,0,0]) cylinder(h=recThickness,r=5,center=true,$fn=50);
union(){
rotate([90,0,0]) cylinder(h=recThickness,r=2.5,center=true,$fn=50);
translate([-(2.5/2)-(2.5),0,0]) cube([2.5+.1,recThickness,0.8],center=true);
}
}
}

module pumpHolder(){
translate([0,0,(topPlateHeight/2) + recHeight/2 ]) union(){
difference(){
    color("red") cube([recWidth,recThickness,topPlateHeight ],center=true);

translate([0,0,-(topPlateHeight/2)+(semiCircleRadius) +topPlateOffset+5 + 2.75]) union(){
translate([0,0, semiCircleRadius/2]) cube([semiCircleDiameter,recThickness,semiCircleRadius],center=true); //topPlateHeight/2+5
rotate([90,0,0]) cylinder(h=recThickness,r=semiCircleRadius,center=true);
}

}
union(){
translate([(hookWidth/2)+(recWidth/2),0,((hookHeight+2)/2)]) recStopper();

translate([-5 - (recWidth/2) +1,0,((hookHeight+2)/2)]) circleStopper();
}
}
}



module endPiece(){
    union(){
        endPieceBlock();
        pumpHolder();
    }
}



difference(){

    endPiece();
       height=59.35 - 2.4;
width=47.60;
thickness=10.65;

topWidth=38.29;
topHeight=23.70;
bottomWidth=31.10;
bottomHeight=height-topHeight;
thickness3=6.57;



diameter=28.88;



circleThickness=2;
radius=diameter/2 + 1;

smallRecHeight=8.38;
smallRecWidth=3.33;
cuttingWidth=23.59;
cuttingHeight=14.69;
extraHeight = (height - (smallRecHeight + cuttingHeight));
extraWidth = 3.63;

bigCircleDiameter=27.33;
topHalfHeight=29.63;
remaindingHeight=height-topHalfHeight;

hex_nut_diameter=7.89 + 1.6; // +1.6, 
hex_nut_radius=hex_nut_diameter/2;
hex_nut_thickness=3.85;

hex_nut_inner_diameter= 5.8;//5;
hex_nut_inner_radius=hex_nut_inner_diameter/2 + .4;



temp=(thickness/2) - (thickness - thickness3);
offsetFromCenter=19; //19.25; //1.5 // 2.3
hexNutGroveExtraDepth=2;

screwRadius=1.75;
screwDepth=9.35;

translate([-4.5,0,-17+1.9 + 1 ]) union(){
    rotate([90,0,0]) translate([(width/2) - (topWidth/2),-(extraHeight - (height/2) - offsetFromCenter) ,-1.5]) cylinder(d=21.95 + .1,h=7,$fn=50,center=true);
    
    rotate([90,0,0]) translate([(width/2) - (topWidth/2),-(extraHeight - (height/2) - offsetFromCenter),0]) cylinder(h=15,d=10 + .2 ,$fn=50,center=true);
    
//    rotate([90,0,0]) union(){
//translate([(width/2) - (topWidth/2),-(extraHeight - (height/2) - offsetFromCenter)-7.75 ,0]) cylinder(h=15,d=3.75,$fn=50,center=true);
//translate([(width/2) - (topWidth/2) -7.75 ,-(extraHeight - (height/2) - offsetFromCenter),0]) cylinder(h=15,d=3.75,$fn=50,center=true);
//translate([(width/2) - (topWidth/2) +7.75 ,-(extraHeight - (height/2) - offsetFromCenter),0]) cylinder(h=15,d=3.75,$fn=50,center=true);
//translate([(width/2) - (topWidth/2) ,-(extraHeight - (height/2) - offsetFromCenter) + 7.75 ,0]) cylinder(h=15,d=3.75,$fn=50,center=true);
//}
    
}

}


//difference(){
//    height=59.35 - 2.4;
//width=47.60;
//thickness=10.65;
//
//topWidth=38.29;
//topHeight=23.70;
//bottomWidth=31.10;
//bottomHeight=height-topHeight;
//thickness3=6.57;
//
//
//
//diameter=28.88;
//
//
//
//circleThickness=2;
//radius=diameter/2 + 1;
//
//smallRecHeight=8.38;
//smallRecWidth=3.33;
//cuttingWidth=23.59;
//cuttingHeight=14.69;
//extraHeight = (height - (smallRecHeight + cuttingHeight));
//extraWidth = 3.63;
//
//bigCircleDiameter=27.33;
//topHalfHeight=29.63;
//remaindingHeight=height-topHalfHeight;
//
//hex_nut_diameter=7.89 + 1.6; // +1.6, 
//hex_nut_radius=hex_nut_diameter/2;
//hex_nut_thickness=3.85;
//
//hex_nut_inner_diameter= 5.8;//5;
//hex_nut_inner_radius=hex_nut_inner_diameter/2 + .4;
//
//
//
//temp=(thickness/2) - (thickness - thickness3);
//offsetFromCenter=19; //19.25; //1.5 // 2.3
//hexNutGroveExtraDepth=2;
//
//screwRadius=1.75;
//screwDepth=9.35;
//difference(){
////union(){
//translate([(width/2) - (topWidth/2),-(extraHeight - (height/2) - offsetFromCenter) ,-1.5]) cylinder(d=21.95 + .2,h=3.5,$fn=50,center=true);
//    
//    translate([(width/2) - (topWidth/2),-(extraHeight - (height/2) - offsetFromCenter),0]) cylinder(h=15,d=10 + .2 ,$fn=50,center=true);
////}
//
//
//}
//
//
//
//
//union(){
//translate([(width/2) - (topWidth/2),-(extraHeight - (height/2) - offsetFromCenter)-7.75 ,0]) cylinder(h=15,d=3.75,$fn=50,center=true);
//translate([(width/2) - (topWidth/2) -7.75 ,-(extraHeight - (height/2) - offsetFromCenter),0]) cylinder(h=15,d=3.75,$fn=50,center=true);
//translate([(width/2) - (topWidth/2) +7.75 ,-(extraHeight - (height/2) - offsetFromCenter),0]) cylinder(h=15,d=3.75,$fn=50,center=true);
//translate([(width/2) - (topWidth/2) ,-(extraHeight - (height/2) - offsetFromCenter) + 7.75 ,0]) cylinder(h=15,d=3.75,$fn=50,center=true);
//}
//
//}







//difference(){
//    //hookHeight+2
//%cube([hookWidth,recThickness,hookHeight+2],center=true);
//
//translate([(stopperWidth/2) + (hookWidth/2)-(stopperWidth),0,-stopperHeight/2]) union(){
//%cube([stopperWidth,recThickness,stopperHeight],center=true);
////color("blue") translate([-((1/2)*stopperWidth)/2,0,2*((stopperHeight-1)/2)]) 
//    color("blue") cube([(1/2)*stopperWidth,hookThickness,stopperHeight-1],center=true);
//}
//}



//translate([stopperWidth/2,0,-((hookHeight+2)/4)]) %cube([stopperWidth,recThickness,(hookHeight+2)/2],center=true);
////color("blue") translate([-((1/2)*stopperWidth)/2,0,2*((stopperHeight-1)/2)]) 
//    color("blue") cube([(1/2)*stopperWidth,hookThickness,stopperHeight-1],center=true);
