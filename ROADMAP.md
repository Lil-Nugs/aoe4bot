# AoE4 Bot Development Roadmap

## Phase 1: Foundation & Basic Actions

### Milestone 1.1: Environment Setup
- [x] Project structure
- [ ] Screen capture implementation
- [ ] Input simulation (keyboard/mouse)
- [ ] Game state detection
- [ ] Basic Gym environment wrapper

### Milestone 1.2: Basic Behaviors
**Goal**: Teach AI fundamental early-game actions

#### 1. Scout Management
- **Observation**: Minimap state, scout position
- **Actions**: Move scout, explore fog of war
- **Reward**: Coverage of map, discovering resources
- **Success Criteria**: 80% map revealed in 5 minutes

#### 2. Sheep Collection
- **Observation**: Sheep positions, town center location
- **Actions**: Select scout, move to sheep, return to TC
- **Reward**: Number of sheep near TC
- **Success Criteria**: 8+ sheep gathered in 3 minutes

#### 3. Town Center Avoidance
- **Observation**: Enemy TC position, unit positions
- **Actions**: Move away from danger zones
- **Reward**: -100 for unit deaths, +10 for staying alive
- **Success Criteria**: Scout survives 10+ minutes

#### 4. Villager Production
- **Observation**: Villager queue status, resources
- **Actions**: Click TC, queue villager
- **Reward**: +10 per villager queued, continuous production bonus
- **Success Criteria**: 100% villager queue uptime

### Milestone 1.3: Integration
- [ ] Combine all behaviors in single agent
- [ ] Multi-task reward function
- [ ] Curriculum learning approach
- [ ] Baseline performance metrics

## Phase 2: Intermediate Economy

### Milestone 2.1: Villager Management
- Idle villager detection
- Automatic resource assignment
- Optimal villager distribution (wood/food/gold/stone)

### Milestone 2.2: Build Orders
- Implement scripted build order execution
- Learn timing optimization
- Adapt to disruptions

### Milestone 2.3: Resource Optimization
- Dynamic villager redistribution
- Resource prediction and planning
- Age advancement timing

## Phase 3: Military & Combat

### Milestone 3.1: Army Production
- Unit composition decisions
- Production queuing
- Military building placement

### Milestone 3.2: Basic Combat
- Army movement
- Attack-move mechanics
- Retreat decisions

### Milestone 3.3: Micro Management
- Unit targeting
- Formation control
- Ability usage

## Phase 4: Strategy & Adaptation

### Milestone 4.1: Strategic Decision Making
- Civilization selection
- Opening strategy choice
- Counter-strategies

### Milestone 4.2: Advanced Tactics
- Raiding
- Map control
- Multi-pronged attacks

## Technical Milestones

### Computer Vision
- [ ] Game state OCR (resources, population, time)
- [ ] Unit detection and classification
- [ ] Minimap analysis
- [ ] Building detection

### Performance
- [ ] Optimize inference speed (<100ms per action)
- [ ] Parallel environment training
- [ ] GPU acceleration for vision models

### Evaluation
- [ ] Automated testing against AI opponents
- [ ] Performance benchmarking suite
- [ ] Replay analysis tools

## Success Metrics

### Phase 1 Target
- Consistently reach Feudal Age by 5:00
- Maintain continuous villager production
- Gather 8+ sheep
- Scout 70%+ of map

### Phase 2 Target
- Execute build orders with 90% accuracy
- Maintain <5% villager idle time
- Reach Castle Age efficiently

### Phase 3 Target
- Win 50%+ games against Easy AI
- Win 30%+ games against Medium AI

### Phase 4 Target
- Win 50%+ games against Hard AI
- Demonstrate strategic adaptation
