import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { swarmRouter } from "./routes/swarm";

dotenv.config();

const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

app.use("/api/swarm", swarmRouter);

app.listen(port, () => {
  console.log(`Backend server listening on port ${port}`);
});
