import { Router } from "express";
import { prisma } from "../lib/prisma";
import { runSwarm } from "../services/swarm";
import { swarmEvents } from "../lib/events";

export const swarmRouter = Router();

swarmRouter.post("/", async (req, res) => {
  try {
    const { prompt, workflowRunId } = req.body;

    // Handle resumption
    if (workflowRunId) {
      const existing = await prisma.workflowRun.findUnique({
        where: { id: workflowRunId }
      });
      if (existing) {
        await prisma.workflowRun.update({
          where: { id: workflowRunId },
          data: { status: "RUNNING" }
        });
        runSwarm(null, workflowRunId).catch(console.error);
        return res.json({ workflowRunId });
      }
    }

    // Handle new workflow
    if (!prompt) {
      return res.status(400).json({ error: "Prompt is required" });
    }

    const workflowRun = await prisma.workflowRun.create({
      data: {
        prompt,
        status: "RUNNING",
      },
    });

    runSwarm(prompt, workflowRun.id).catch(console.error);

    res.json({ workflowRunId: workflowRun.id });
  } catch (error) {
    res.status(500).json({ error: "Internal Server Error" });
  }
});

swarmRouter.get("/stream", async (req, res) => {
  const workflowRunId = req.query.workflowRunId as string;

  if (!workflowRunId) {
    return res.status(400).json({ error: "workflowRunId is required" });
  }

  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.flushHeaders();

  // Send existing logs
  const existingRun = await prisma.workflowRun.findUnique({
    where: { id: workflowRunId },
    include: { logs: { orderBy: { createdAt: "asc" } } },
  });

  if (existingRun) {
    for (const log of existingRun.logs) {
      res.write(`data: ${JSON.stringify({ type: "log", data: log })}\n\n`);
    }
    if (existingRun.status !== "RUNNING") {
      res.write(`data: ${JSON.stringify({ type: "status", status: existingRun.status, result: existingRun.result })}\n\n`);
      return res.end();
    }
  }

  // Listen for new logs
  const onLog = (data: any) => {
    if (data.workflowRunId === workflowRunId) {
      res.write(`data: ${JSON.stringify({ type: "log", data })}\n\n`);
    }
  };

  const onStatus = (data: any) => {
    if (data.workflowRunId === workflowRunId) {
      res.write(`data: ${JSON.stringify({ type: "status", status: data.status, result: data.result })}\n\n`);
      res.end();
    }
  };

  swarmEvents.on("log", onLog);
  swarmEvents.on("status", onStatus);

  req.on("close", () => {
    swarmEvents.off("log", onLog);
    swarmEvents.off("status", onStatus);
  });
});

swarmRouter.get("/history", async (req, res) => {
  try {
    const runs = await prisma.workflowRun.findMany({
      orderBy: { createdAt: "desc" },
      take: 20,
    });
    res.json({ runs });
  } catch (error) {
    res.status(500).json({ error: "Internal Server Error" });
  }
});

swarmRouter.get("/logs", async (req, res) => {
  const workflowRunId = req.query.workflowRunId as string;

  if (!workflowRunId) {
    return res.status(400).json({ error: "workflowRunId is required" });
  }

  try {
    const run = await prisma.workflowRun.findUnique({
      where: { id: workflowRunId },
      include: { logs: { orderBy: { createdAt: 'asc' } } },
    });

    if (!run) {
      return res.status(404).json({ error: "Workflow not found" });
    }

    res.json(run);
  } catch (error) {
    res.status(500).json({ error: "Internal Server Error" });
  }
});
