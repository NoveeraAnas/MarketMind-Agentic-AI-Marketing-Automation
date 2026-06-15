# MarketMind: Agentic AI Content Marketing Automation

## Overview

MarketMind is a multi-agent AI system that automates the complete content marketing lifecycle from strategy creation to campaign execution.

## Problem Statement

Small businesses struggle with creating high-quality, consistent marketing content.

## Proposed Solution

MarketMind uses specialized AI agents coordinated by a Supervisor Agent to perform marketing tasks autonomously while keeping a human approval checkpoint before execution.

## Agent Architecture

- Supervisor Agent
- Research Agent
- Strategy Agent
- Content Agent
- Critic Agent
- Instagram Agent
- Scheduler Agent
- Automation Agent (n8n)

## Workflow

User Input
↓
Supervisor Agent
↓
Research Agent
↓
Strategy Agent
↓
Content Agent
↓
Critic Agent
↓
Instagram Agent
↓
Human Approval
↓
Scheduler
↓
n8n Automation
↓
Email Notification

## Technologies

- Python
- Streamlit
- Groq LLM
- n8n
- Webhooks
- Email Automation

## Features

- Multi-agent collaboration
- Campaign generation
- AI content review
- Instagram post generation
- Human-in-the-loop approval
- AI post improvement
- Scheduling
- n8n workflow integration
- Email notifications