import { EventEmitter } from "events";

class SwarmEventEmitter extends EventEmitter {}
export const swarmEvents = new SwarmEventEmitter();
