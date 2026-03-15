https://youtu.be/2iXYEbsW6Yc
Step-by-step guide to test each environment
Maze (Labirinto)

Fixed (LabirintoFix class)

First, add a maze to the file parametros.json with the following exact syntax:

{
    "tipo": "labirinto",
    "labirinto": [
        ["S", 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        ...
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, "E", 0, 0, 0, 0, 1, 0, 1, 1, 1, 1]
    ],
    "max_passos": 800,
    "passo_a_passo": true
}

Run the LabirintoFix class to test the fixed maze scenario.

Evolutionary (LabirintoEvo class)

Use the same maze format in parametros.json.

If you want to change the number of allowed steps, update the max_passos field in parametros.json.

To modify population size or number of training generations, edit the last line of the TrainLab file.

To change the mutation rate or elitism count, edit line 57 in TrainLab.

First, run TrainLab to train the neural network for the selected maze. Various performance metrics and graphs will be generated.

Finally, run the LabirintoEvo class to visualize the results.

Lighthouse (Farol)

Fixed (FarolFix class)

Add a lighthouse environment to parametersFarol.json with the following syntax:

{
  "tipo": "farol",
  "labirinto": [
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,"S",0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,1],
      ...
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
  ],
  "max_passos": 200,
  "passo_a_passo": true
}

Run the FarolFix class to test the fixed lighthouse scenario.

Evolutionary (FarolEvo class)

Use the same environment format in parametersFarol.json.

To change the number of allowed steps, modify max_passos in parametersFarol.json.

To change population size or number of training generations, edit the last line of TrainFarol.

To adjust mutation rate or elitism count, edit line 68 of TrainFarol.

First, run TrainFarol to train the neural network for the selected lighthouse scenario. Various performance graphs will be generated.

Then, run the FarolEvo class to visualize the results.

Notes:

Sometimes, when running the code on a new computer, the simulation engine may fail with the warning: "motor de simulacao nao pode ser criado" (“simulation engine cannot be created”).
In that case, delete and recreate the parametros.json and parametersFarol.json files with the same content.

In the maze (parametros.json), the end position is represented by "E", while in the lighthouse (parametersFarol.json), it is represented by "F".
