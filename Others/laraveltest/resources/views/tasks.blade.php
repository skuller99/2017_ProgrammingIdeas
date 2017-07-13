@extends('layouts.app')

@section('content')
<div class="container">
    <div class="col-sm-offset-2 col-sm-8">
        <div class="panel panel-default">
            <div class="panel-heading" style= "text-align:center; font-weight: bold">
                Nauja užduotis
            </div>

            <div class="panel-body">
                <!-- Display Validation Errors -->
                @include('common.errors')

                <!-- New Task Form -->
                <form action="{{ url('task')}}" method="POST" class="form-horizontal">
                    {{ csrf_field() }}

                    <!-- Task Name -->
                    <div class="form-group">
                        <label for="task-name" class="col-sm-3 control-label">Užduotis</label>

                        <div class="col-sm-6">
                            <input type="text" name="name" id="task-name" class="form-control" value="{{ old('task') }}">
                        </div>
                    </div>

                    <!-- Add Task Button -->
                    <div class="form-group">
                        <div class="col-sm-offset-3 col-sm-6">
                            <button type="submit" class="btn btn-default">
                                <i class="fa fa-btn fa-plus"></i>Pridėti užduotį
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <!-- Current Tasks -->
        @if (count($tasks) > 0)
        <div class="panel panel-default">
            <div class="panel-heading" style= "text-align:center; font-weight: bold">
                Užduočių sąrašas
            </div>

            <div class="panel-body">
                <table class="table table-striped task-table">
                    <thead>
                        <th>Numeris</th>
                        <th>Užduotis</th>
                        <th>Sukūrimo data</th>
                        <th>Statusas</th>
                        <th>&nbsp;</th>

                    </thead>
                    <tbody>
                        @foreach ($tasks as $task)
                        <tr>
                            <td class="table-text"><div>{{ $task->id }}</div></td>
                            <td class="table-text"><div>{{ $task->name }}</div></td>

                            <?php
                            // Datos užrašymas nustatytu formatu
                            $creationDate = date("Y-m-d", strtotime($task->created_at));
                            ?>
                            <td class="table-text"><div>{{ $creationDate }}</div></td>

                            <!-- Task status button-->

                            <td>
                                <?php
                                // Langelis pateikiamas priklausomai nuo užduoties statuso

                                if ( $task->status  == 0){
                                    $klase = "btn btn-primary";
                                    $tekstas = "Neatlikta";
                                }
                                else if ( $task->status  == 1){
                                    $klase = "btn btn-success";
                                    $tekstas = "Atlikta";
                                }       

                                ?>                              
                                <form action="{{ url('task/'.$task->id) }}" 
                                      method="POST"> {{ csrf_field() }} 

                                    <button type="submit" class="<?php echo $klase ?>" name="complete"
                                            style="margin-left:20px; padding: 10px">
                                        <?php echo $tekstas ?>
                                    </button>
                                </form> 
                            </td>

                            <!-- Task Delete Button -->
                            <td>
                                <form action="{{ url('task/'.$task->id) }}" method="POST">
                                    {{ csrf_field() }}
                                    {{ method_field('DELETE') }}

                                    <button type="submit" class="btn btn-danger" 
                                            style="margin-left:20px; padding: 10px">
                                        <i class="fa fa-btn fa-trash"></i>Ištrinti
                                    </button>
                                </form>
                            </td>
                        </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>
        </div>
        @endif
    </div>
</div>
@endsection