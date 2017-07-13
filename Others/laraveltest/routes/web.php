<?php
/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| This route group applies the "web" middleware group to every route
| it contains. The "web" middleware group is defined in your HTTP
| kernel and includes session state, CSRF protection, and more.
|
*/
use App\Task;
use Illuminate\Http\Request;

/*Route::get('/', function () {
    return view('welcome');
});*/

/*Route::get('/hello',function(){
    return 'Hello World!';
});*/

Route::get('hello', 'Hello@index');
Route::get('/hello/{name}', 'Hello@show');


Route::group(['middleware' => ['web']], function () {
    /**
     * Show Task Dashboard
     */
    Route::get('/', function () {
        return view('tasks', [
            'tasks' => Task::orderBy('created_at', 'asc')->get()
        ]);
    });
    /**
     * Add New Task
     */
    Route::post('/task', function (Request $request) {
        $validator = Validator::make($request->all(), [
            'name' => 'required|max:255',
        ]);
        if ($validator->fails()) {
            return redirect('/')
                ->withInput()
                ->withErrors($validator);
        }
        $task = new Task;
        $task->name = $request->name;
        $task->save();
        return redirect('/');
    });
    
    /**
    Mark as complete
    */
    Route::post('/task/{id}', function ($id) {
        $task = Task::findOrFail($id);
        if ($task->status==0){
            $task->status = 1;
        }
        else
            $task->status = 0;   
        
        $task->save();
        return redirect('/');
    });
                
    
    
    /**
     * Delete Task
     */
    Route::delete('/task/{id}', function ($id) {
        Task::findOrFail($id)->delete();
        return redirect('/');
    });
}); 