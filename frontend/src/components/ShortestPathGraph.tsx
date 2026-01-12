import React, { useMemo, useRef, useEffect } from "react";
import ForceGraph2D, { type ForceGraphMethods } from "react-force-graph-2d";
import * as d3 from "d3-force";

interface PathGraphProps {
  pathData: any[];
}

const ShortestPathGraph: React.FC<PathGraphProps> = ({ pathData }) => {
  const forceRef = useRef<ForceGraphMethods<any, any> | undefined>(undefined);

  useEffect(() => {
    const forceRefCurrent = forceRef.current;
    if (forceRefCurrent) {
      // remove center force
      forceRefCurrent.d3Force("center", null);

      //push each node to its linear order
      forceRefCurrent.d3Force(
        "x",
        d3
          .forceX((d: any) => (d.order - (pathData.length - 1) / 2) * 200)
          .strength(0.05)
      );

      // center in the y direction
      forceRefCurrent.d3Force("y", d3.forceY(0).strength(0.05));

      // make nodes collide
      forceRefCurrent.d3Force("collide", d3.forceCollide(50));

      // set the distance and strength of each edge
      (forceRefCurrent.d3Force("link") as any)?.distance(100).strength(0.05);

      // add a timeout as drawing the nodes takes time, and we want to center after they have all been drawn
      setTimeout(() => {
        forceRefCurrent.zoomToFit(400, 150);
      }, 500);
    }
  }, [pathData]);

  const graphData = useMemo(() => {
    // create the nodes (each must have a unique id)
    const nodes = pathData.map((item, index) => {
      // redirect to the image-proxy endpoint to workaround CORS restrictions
      const image = new Image();
      // depending on if the current node is a player or a team, the image attribute will be different
      const encodedUrl = encodeURIComponent(
        index % 2 == 0 ? item.headshot_url : item.logo_url
      );
      image.src = `${import.meta.env.VITE_BASE_API_URL}image-proxy/?image_url=${encodedUrl}`;

      return {
        id: item.id,
        name: item.full_name,
        order: index,
        type: index % 2 === 1 ? "team" : "player",
        image: image,
      };
    });

    // create the links (each must have a source and target id matching the ids used above)
    const links = pathData.slice(0, -1).map((_, i) => ({
      source: pathData[i].id,
      target: pathData[i + 1].id,
    }));

    return { nodes, links };
  }, [pathData]);

  return (
    <div style={{ width: "100%", height: "600px" }}>
      <ForceGraph2D
        ref={forceRef}
        graphData={graphData}
        backgroundColor="#1a1a1a"
        linkColor={() => "#D3D3D3"}
        linkWidth={2}
        linkDirectionalParticles={2}
        linkDirectionalParticleWidth={10}
        linkDirectionalParticleColor={() => "#D1D7DB"}
        linkDirectionalParticleSpeed={0.005}
        d3AlphaDecay={0.05}
        nodeCanvasObject={(node: any, ctx, globalScale) => {
          // make the team node bigger as the logos tend to be bigger images and do not scale well
          const size = node.type === "team" ? 18 : 14;
          const fontSize = 13 / globalScale;

          ctx.save();
          ctx.beginPath();
          // draw each node as a filled-in circle
          ctx.arc(node.x, node.y, size, 0, 2 * Math.PI, false);
          ctx.clip();
          ctx.fillStyle = "#333";
          ctx.fill();

          // draw the image for the team or player if it is valid
          if (
            node.image &&
            node.image.complete &&
            node.image.naturalWidth !== 0
          ) {
            ctx.drawImage(
              node.image,
              node.x - size,
              node.y - size,
              size * 2,
              size * 2
            );
          }

          ctx.restore();

          // color code the borders (simple for now, will be updated based on team)
          ctx.beginPath();
          ctx.arc(node.x, node.y, size, 0, 2 * Math.PI, false);
          ctx.lineWidth = 2 / globalScale;
          ctx.strokeStyle = node.type === "player" ? "#888" : "#FFF";
          ctx.stroke();

          // add a new line for each space as text gets jumbled
          ctx.font = `${fontSize}px Sans-Serif`;
          ctx.textAlign = "center";
          ctx.textBaseline = "top";
          ctx.fillStyle = "#EEE";
          const lines = node.name.split(" ");
          lines.forEach((line: string, i: number) => {
            ctx.fillText(
              line,
              node.x,
              node.y + size + 6 + i * (fontSize * 1.2)
            );
          });
        }}
      />
    </div>
  );
};

export default ShortestPathGraph;
